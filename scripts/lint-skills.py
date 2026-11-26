#!/usr/bin/env python3
"""Mechanischer Frontmatter-Lint fuer die Kit-Skills (skills/dtb-*/SKILL.md).

Prueft die eindeutigen Regeln aus skills/CLAUDE.md -> "Frontmatter (Pflichtfelder)".
Einstufung wie dtb:project-health Check 8, ergaenzt um Praefix, Stage, Laenge,
Werkzeug-Pflicht und Gegenkante als FEHLER.

Aufruf:  python scripts/lint-skills.py [REPO-ROOT]
         (ohne -I: -I blendet die User-site-packages aus, PyYAML fehlt dann)
         --ohne-ausnahmen  nur fuer den Selbsttest: prueft ohne EDGE_EXCEPTIONS
                           (Fixture-Baeume kennen die Kit-Skills der Ausnahmeliste nicht)
Exit:    0 = kein FEHLER, 1 = mindestens ein FEHLER, 2 = Aufruf-/Umgebungsfehler
Ausgabe: je Befund eine Zeile "{FEHLER|WARNUNG} {skill}: {regel} — {detail}"
         (das Detail enthaelt selbst kein " — "), danach eine Schlusszeile mit Zaehlern.

Regel-Aenderungen in skills/CLAUDE.md ziehen dieses Skript im selben Zug mit.
"""

import sys

sys.dont_write_bytecode = True

import os
import re
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:  # pragma: no cover - sehr alte Python-Versionen
    pass

try:
    import yaml
except ImportError:
    print(
        "lint-skills: PyYAML fehlt — installieren mit: pip install pyyaml "
        "(und ohne 'python -I' aufrufen)",
        file=sys.stderr,
    )
    sys.exit(2)


STAGES = (
    "idea", "capture", "planning", "implementation", "execution",
    "development", "session", "monitoring", "setup", "greenfield",
)
MAX_DESCRIPTION = 350
COUNTER_FIELD = {"next": "after", "after": "next"}

# Bewusst einseitige Pipeline-Kanten: (Quelle, Feld, Ziel, Grund).
# Jeder Eintrag braucht einen Grund; ein Eintrag, der keine einseitige Kante
# mehr deckt, wird als WARNUNG gemeldet und gehoert dann entfernt.
EDGE_EXCEPTIONS = (
    ("dtb:meeting-dump", "next", "dtb:workflow-next",
     "workflow-next ist eine jederzeit aufrufbare Lese-Sicht ohne Pipeline-Vorgaenger; "
     "die Kante heisst 'danach nachsehen', keine Station (entschieden 2026-11-26)"),
    ("dtb:open-question", "next", "dtb:workflow-next",
     "workflow-next ist eine jederzeit aufrufbare Lese-Sicht ohne Pipeline-Vorgaenger; "
     "die Kante heisst 'danach nachsehen', keine Station (entschieden 2026-11-26)"),
)

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)
# Shell-Block, Voll-Guard und Teil-Guard verlangen Bash. Bewusst akzeptiertes
# Falsch-Positiv: ein Anker, der in einer aeusseren (Vier-Backtick-)Fence nur zitiert wird.
SHELL_FENCE_RE = re.compile(r"^[ \t]*(?:```|~~~)(?:bash|sh|shell)\b", re.M)
GUARD_RE = re.compile(r"^#{2,3} Worktree-Guard\b", re.M)
PART_GUARD_RE = re.compile(r"^[ \t]*\*\*Teil-Guard \(Worktree\):\*\*", re.M)


class UsageError(Exception):
    """Aufruf- oder Umgebungsfehler (Exit 2)."""


class Report:
    def __init__(self):
        self.lines = []
        self.errors = 0
        self.warnings = 0

    def error(self, skill, rule, detail):
        self.errors += 1
        self.lines.append(f"FEHLER {skill}: {rule} — {detail}")

    def warning(self, skill, rule, detail):
        self.warnings += 1
        self.lines.append(f"WARNUNG {skill}: {rule} — {detail}")


def read_skill(path):
    """Liefert (frontmatter-dict | None, body, fehlertext | None)."""
    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        return None, "", f"Datei ist kein UTF-8 ({exc.reason})"
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text, "kein Frontmatter-Block (--- … ---) am Dateianfang"
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        first = str(exc).strip().splitlines()[0]
        return None, text[match.end():], f"Frontmatter ist kein gueltiges YAML ({first})"
    if not isinstance(data, dict):
        return None, text[match.end():], "Frontmatter ist kein YAML-Mapping"
    return data, text[match.end():], None


def tool_list(value):
    """Werkzeugnamen ohne Muster-Zusatz: 'Bash(git:*)' zaehlt als 'Bash'."""
    if value is None:
        return []
    items = value if isinstance(value, (list, tuple)) else str(value).split(",")
    return [str(item).split("(")[0].strip() for item in items]


def folded(text):
    """Faltung laut skills/CLAUDE.md: Zeilenumbruch + Einrueckung = ein Leerzeichen."""
    return re.sub(r"\n[ \t]*", " ", text).strip()


def skill_dir_for(name):
    """dtb:foo -> dtb-foo; None, wenn der Name kein dtb:-Name ist."""
    if not isinstance(name, str) or not name.startswith("dtb:") or len(name) <= 4:
        return None
    return "dtb-" + name[4:]


def lint(root, exceptions=EDGE_EXCEPTIONS):
    report = Report()
    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        raise UsageError(f"kein Ordner skills/ unter {root}")

    dirs = sorted(
        entry for entry in os.listdir(skills_dir)
        if entry.startswith("dtb-") and os.path.isdir(os.path.join(skills_dir, entry))
    )
    existing = set()
    # Verzeichnis -> pipeline-Block: dict (fehlender Block = {}), None bei ungueltigem Block
    pipelines = {}

    for skill in dirs:
        path = os.path.join(skills_dir, skill, "SKILL.md")
        if not os.path.isfile(path):
            report.error(skill, "skill-md-fehlt", "Verzeichnis ohne SKILL.md")
            continue
        existing.add(skill)
        data, body, problem = read_skill(path)
        if problem:
            report.error(skill, "frontmatter", problem)
            continue
        pipelines[skill] = check_skill(report, skill, data, body)

    allowed = {(source, field, target) for source, field, target, _ in exceptions}
    for skill in sorted(pipelines):
        if pipelines[skill] is not None:
            check_edges(report, skill, pipelines, existing, allowed)
    check_exceptions(report, pipelines, exceptions)
    return len(dirs), report


def check_skill(report, skill, data, body):
    """Feld-Regeln eines Skills; liefert den pipeline-Block ({} wenn fehlend, None wenn ungueltig)."""
    name = data.get("name")
    if name is None:
        report.error(skill, "name-fehlt", "Feld name fehlt")
    elif name != "dtb:" + skill[4:]:
        report.error(skill, "name-verzeichnis", f"name '{name}' passt nicht zu dtb:{skill[4:]}")

    description = data.get("description")
    if description is None:
        report.error(skill, "description-fehlt", "Feld description fehlt")
    elif not isinstance(description, str):
        report.error(skill, "use-when", "description ist kein Text")
        description = None
    elif not folded(description).startswith("Use when:"):
        report.error(skill, "use-when", "description beginnt nicht mit 'Use when:'")

    # Nur ein echtes `true` schaltet den Modell-Aufruf ab: fehlt das Feld oder ist es kein
    # Bool, laedt Claude Code die Beschreibung trotzdem in jede Session -> Laenge zaehlt.
    dmi = data.get("disable-model-invocation")
    if "disable-model-invocation" not in data:
        report.warning(skill, "feld-fehlt", "disable-model-invocation fehlt (gilt als false)")
    elif not isinstance(dmi, bool):
        report.error(skill, "dmi-typ", f"disable-model-invocation ist kein Bool ({dmi!r})")
    if dmi is not True and description is not None:
        length = len(folded(description))
        if length > MAX_DESCRIPTION:
            report.error(
                skill, "beschreibung-laenge",
                f"{length} Zeichen (gefaltet) > {MAX_DESCRIPTION} bei modellaufrufbarem Skill "
                "(disable-model-invocation nicht true)",
            )

    if "allowed-tools" not in data:
        report.warning(skill, "feld-fehlt", "allowed-tools fehlt")
    tools = tool_list(data.get("allowed-tools"))
    reasons = []
    if SHELL_FENCE_RE.search(body):
        reasons.append("Shell-Block")
    if GUARD_RE.search(body):
        reasons.append("Worktree-Guard")
    if PART_GUARD_RE.search(body):
        reasons.append("**Teil-Guard (Worktree):**")
    if reasons and "Bash" not in tools:
        report.error(skill, "werkzeug-bash", f"Bash fehlt in allowed-tools ({', '.join(reasons)})")

    if "pipeline" not in data:
        report.warning(skill, "feld-fehlt", "pipeline fehlt")
        return {}
    pipeline = data["pipeline"]
    if not isinstance(pipeline, dict):
        report.error(skill, "pipeline", "pipeline ist kein Block")
        return None

    stage = pipeline.get("stage")
    if stage not in STAGES:
        report.error(skill, "stage", f"stage '{stage}' nicht im Wertebereich ({', '.join(STAGES)})")

    for field in COUNTER_FIELD:
        value = pipeline.get(field)
        if value is not None and not isinstance(value, list):
            report.error(skill, "listenform", f"{field} ist weder Liste noch null")
    return pipeline


def edge_list(pipeline, field):
    """Kanten eines Feldes; None, wenn das Feld weder Liste noch null ist (eigener FEHLER)."""
    value = pipeline.get(field)
    if value is None:
        return []
    return value if isinstance(value, list) else None


def check_edges(report, skill, pipelines, existing, allowed):
    own_name = "dtb:" + skill[4:]
    for field, counter in COUNTER_FIELD.items():
        for target in edge_list(pipelines[skill], field) or []:
            target_dir = skill_dir_for(target)
            if target_dir is None or target_dir not in existing:
                report.error(skill, "kanten-ziel", f"{field}: {target} (kein Skill skills/{target_dir or target}/SKILL.md)")
                continue
            target_pipeline = pipelines.get(target_dir)
            if target_pipeline is None:
                continue  # Ziel hat selbst einen Frontmatter- oder pipeline-FEHLER
            back = edge_list(target_pipeline, counter)
            if back is None:
                continue  # Gegenfeld ist keine Liste: Ziel traegt dafuer schon `listenform`
            if own_name in back or (own_name, field, target) in allowed:
                continue
            report.error(
                skill, "gegenkante",
                f"{field}: {target}, aber {target}.{counter} nennt {own_name} nicht "
                "(Gegenkante ergaenzen oder in EDGE_EXCEPTIONS mit Grund fuehren)",
            )


def check_exceptions(report, pipelines, exceptions):
    for source, field, target, reason in exceptions:
        label = f"EDGE_EXCEPTIONS {source}.{field} -> {target}"
        if not str(reason).strip():
            report.error("lint-skills", "ausnahme-grund", f"{label} ohne Grund")
        counter = COUNTER_FIELD.get(field)
        if counter is None:
            report.error("lint-skills", "ausnahme-feld", f"{label}: Feld muss next oder after sein")
            continue
        source_pipeline = pipelines.get(skill_dir_for(source))
        target_pipeline = pipelines.get(skill_dir_for(target))
        if source_pipeline is None or target_pipeline is None:
            report.warning("lint-skills", "ausnahme-ueberfluessig", f"{label}: Quelle oder Ziel fehlt")
        elif target not in (edge_list(source_pipeline, field) or []):
            report.warning("lint-skills", "ausnahme-ueberfluessig", f"{label}: deckt keine bestehende Kante")
        elif source in (edge_list(target_pipeline, counter) or []):
            report.warning("lint-skills", "ausnahme-ueberfluessig", f"{label}: Gegenkante existiert inzwischen")


def main(argv):
    args = list(argv[1:])
    exceptions = EDGE_EXCEPTIONS
    if "--ohne-ausnahmen" in args:
        args.remove("--ohne-ausnahmen")
        exceptions = ()
    if len(args) > 1:
        print("Aufruf: python scripts/lint-skills.py [REPO-ROOT]", file=sys.stderr)
        return 2
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(args[0]) if args else default_root
    try:
        count, report = lint(root, exceptions)
    except UsageError as exc:
        print(f"lint-skills: {exc}", file=sys.stderr)
        return 2
    except Exception:  # unerwartet: nie als Exit 1 (= "FEHLER gefunden") ausgeben
        traceback.print_exc()
        print("lint-skills: unerwarteter Fehler — Lauf abgebrochen", file=sys.stderr)
        return 2
    for line in report.lines:
        print(line)
    print(f"lint-skills: {count} Skills geprueft, {report.errors} FEHLER, {report.warnings} WARNUNG(EN)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
