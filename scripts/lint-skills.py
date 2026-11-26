#!/usr/bin/env python3
"""Mechanischer Frontmatter-Lint fuer die Kit-Skills (skills/dtb-*/SKILL.md).

Prueft die eindeutigen Regeln aus skills/CLAUDE.md -> "Frontmatter (Pflichtfelder)".
Einstufung wie dtb:project-health Check 8, ergaenzt um Praefix, Stage, Laenge,
Werkzeug-Pflicht und Gegenkante als FEHLER.

Aufruf:  python scripts/lint-skills.py [REPO-ROOT]
         (ohne -I: -I blendet die User-site-packages aus, PyYAML fehlt dann)
Exit:    0 = kein FEHLER, 1 = mindestens ein FEHLER, 2 = Aufruf-/Umgebungsfehler
Ausgabe: je Befund eine Zeile "{FEHLER|WARNUNG} {skill}: {regel} — {detail}",
         danach eine Schlusszeile mit Zaehlern.

Regel-Aenderungen in skills/CLAUDE.md ziehen dieses Skript im selben Zug mit.
"""

import sys

sys.dont_write_bytecode = True

import os
import re

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
EDGE_FIELDS = (("next", "after"), ("after", "next"))

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
BASH_FENCE_RE = re.compile(r"^[ \t]*```bash\b", re.M)
GUARD_RE = re.compile(r"^## Worktree-Guard\b", re.M)
PART_GUARD_RE = re.compile(r"^[ \t]*\*\*Teil-Guard \(Worktree\):\*\*", re.M)


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
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value]
    return [item.strip() for item in str(value).split(",")]


def folded(text):
    return re.sub(r"\s+", " ", text).strip()


def skill_dir_for(name):
    """dtb:foo -> dtb-foo; None, wenn der Name kein dtb:-Name ist."""
    if not isinstance(name, str) or not name.startswith("dtb:") or len(name) <= 4:
        return None
    return "dtb-" + name[4:]


def lint(root):
    report = Report()
    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        print(f"lint-skills: kein Ordner skills/ unter {root}", file=sys.stderr)
        sys.exit(2)

    dirs = sorted(
        entry for entry in os.listdir(skills_dir)
        if entry.startswith("dtb-") and os.path.isdir(os.path.join(skills_dir, entry))
    )
    existing = set()
    parsed = {}  # Verzeichnis -> (frontmatter, pipeline-dict | None)

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
        parsed[skill] = (data, check_skill(report, skill, data, body))

    for skill in sorted(parsed):
        data, pipeline = parsed[skill]
        if pipeline is not None:
            check_edges(report, skill, pipeline, existing, parsed)
    check_exceptions(report, parsed)
    return len(dirs), report


def check_skill(report, skill, data, body):
    """Feld-Regeln eines Skills; liefert den pipeline-Block (oder None)."""
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

    if "disable-model-invocation" not in data:
        report.warning(skill, "feld-fehlt", "disable-model-invocation fehlt")
    elif data["disable-model-invocation"] is False and description is not None:
        length = len(folded(description))
        if length > MAX_DESCRIPTION:
            report.error(
                skill, "beschreibung-laenge",
                f"{length} Zeichen (gefaltet) > {MAX_DESCRIPTION} bei disable-model-invocation: false",
            )

    if "allowed-tools" not in data:
        report.warning(skill, "feld-fehlt", "allowed-tools fehlt")
    tools = tool_list(data.get("allowed-tools"))
    reasons = []
    if BASH_FENCE_RE.search(body):
        reasons.append("```bash-Block")
    if GUARD_RE.search(body):
        reasons.append("## Worktree-Guard")
    if PART_GUARD_RE.search(body):
        reasons.append("**Teil-Guard (Worktree):**")
    if reasons and "Bash" not in tools:
        report.error(skill, "werkzeug-bash", f"Bash fehlt in allowed-tools ({', '.join(reasons)})")

    if "pipeline" not in data:
        report.warning(skill, "feld-fehlt", "pipeline fehlt")
        return None
    pipeline = data["pipeline"]
    if not isinstance(pipeline, dict):
        report.error(skill, "pipeline", "pipeline ist kein Block")
        return None

    stage = pipeline.get("stage")
    if stage not in STAGES:
        report.error(skill, "stage", f"stage '{stage}' nicht im Wertebereich ({', '.join(STAGES)})")

    for field, _ in EDGE_FIELDS:
        value = pipeline.get(field)
        if value is not None and not isinstance(value, list):
            report.error(skill, "listenform", f"{field} ist weder Liste noch null")
    return pipeline


def edge_list(pipeline, field):
    value = pipeline.get(field) if isinstance(pipeline, dict) else None
    return value if isinstance(value, list) else []


def check_edges(report, skill, pipeline, existing, parsed):
    own_name = "dtb:" + skill[4:]
    for field, counter in EDGE_FIELDS:
        for target in edge_list(pipeline, field):
            target_dir = skill_dir_for(target)
            if target_dir is None or target_dir not in existing:
                report.error(skill, "kanten-ziel", f"{field}: {target} — kein Skill skills/{target_dir or target}/SKILL.md")
                continue
            if target_dir not in parsed:
                continue  # Ziel hat selbst einen Frontmatter-FEHLER
            back = edge_list(parsed[target_dir][1], counter)
            if own_name in back or (own_name, field, target) in exception_keys():
                continue
            report.error(
                skill, "gegenkante",
                f"{field}: {target}, aber {target}.{counter} nennt {own_name} nicht "
                "(Gegenkante ergaenzen oder in EDGE_EXCEPTIONS mit Grund fuehren)",
            )


def exception_keys():
    return {(source, field, target) for source, field, target, _ in EDGE_EXCEPTIONS}


def check_exceptions(report, parsed):
    for source, field, target, reason in EDGE_EXCEPTIONS:
        label = f"EDGE_EXCEPTIONS ({source}.{field} -> {target})"
        if not str(reason).strip():
            report.error("lint-skills", "ausnahme-grund", f"{label} ohne Grund")
        source_dir = skill_dir_for(source)
        target_dir = skill_dir_for(target)
        counter = dict(EDGE_FIELDS).get(field)
        if source_dir not in parsed and target_dir not in parsed:
            continue  # fremder Baum (z.B. Selbsttest-Fixture): die Ausnahme betrifft ihn nicht
        if source_dir not in parsed or target_dir not in parsed or counter is None:
            report.warning("lint-skills", "ausnahme-ueberfluessig", f"{label} deckt keine bestehende Kante")
            continue
        if target not in edge_list(parsed[source_dir][1], field):
            report.warning("lint-skills", "ausnahme-ueberfluessig", f"{label} deckt keine bestehende Kante")
        elif source in edge_list(parsed[target_dir][1], counter):
            report.warning("lint-skills", "ausnahme-ueberfluessig", f"{label} — Gegenkante existiert inzwischen")


def main(argv):
    if len(argv) > 2:
        print("Aufruf: python scripts/lint-skills.py [REPO-ROOT]", file=sys.stderr)
        return 2
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(argv[1]) if len(argv) == 2 else default_root
    count, report = lint(root)
    for line in report.lines:
        print(line)
    print(f"lint-skills: {count} Skills geprueft, {report.errors} FEHLER, {report.warnings} WARNUNG(EN)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
