"""Zeit je Teil von dtb:workflow-checkpoint aus Claude-Code-Transkripten messen (read-only).

Entstanden in der Erhebung zu #177 (Checkpoint schneller), 2026-11-02. Liest nur, schreibt nichts.

Aufruf (aus dem Projekt-Root, Python 3.9+):
    python -I dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py
    ... -v             zusaetzlich eine Tabellenzeile je Lauf
    ... --rueckfragen  zusaetzlich Wartezeit nach Art der Rueckfrage (nur Zahlen und Kategorien)
    ... --auszuege     zusaetzlich Klartext-Auszuege je Antwort (Frage des Modells + Antwort)

WARNUNG zu --auszuege: Die Auszuege stammen aus fremden Sitzungen aller Projekte unter
~/.claude/projects und enthalten Personennamen und Fachinhalte. Nur in der Konsole ansehen, nie in
versionierte Dateien, Logs oder Chats kopieren; Namen vor jeder Weitergabe durch Rollen ersetzen.

Begriffe:
- Segment: vom Slash-Befehl workflow-checkpoint bis zum naechsten Slash-Befehl, zum naechsten
  Ketten-Skill (Skill-Aufruf des Modells) oder zum Sitzungsende — dieselbe Abgrenzung wie
  chain-metrics.py im Nachbar-Repo mega.dev, dessen "aktive min" die Zielgroesse von #177 sind.
- Kern: vom Start bis zum letzten Schreibvorgang des Checkpoints (Write/Edit auf Changelog,
  WORKFLOW_STATUS, Dashboard-Seite, lessons.md, INBOX*), verlaengert bis zur ersten Modell-Nachricht
  mit Text danach (die Bestaetigung aus Schritt 6).
  Segment minus Kern = Nachlauf (z. B. Commit-Frage, Folgearbeit in derselben Sitzung).
- Aktive Zeit: Summe der Luecken zwischen Ereignissen, jede Luecke hoechstens 300 s.
- Phase einer Luecke: die Phase des Ereignisses, das die Luecke beendet; Luecken vor einer
  Antwort des Menschen (Freitext oder Ergebnis einer Auswahlfrage) zaehlen als "Mensch".
- Arten: worktree = Abbruch durch den Voll-Guard (Sende-Seite); ohne_kern = kein Schreibvorgang;
  handoff = Empfang eines WORKTREE-HANDOFF-Blocks; normal = alles andere. Ausgewertet werden
  normal + handoff mit Kern.

Grenzen (benannt):
- Die Phasen-Zuordnung ist eine Heuristik ueber Werkzeug und Pfad (classify). Projekte mit
  abweichendem Changelog- oder Status-Pfad landen bei Log/Status zu niedrig, ihre Zeit faellt in
  die vorherige Phase.
- Die Rueckfrage-Kategorien sind Textmuster ueber das Ende der vorangehenden Modell-Nachricht.
- Nur Hauptsitzungen (keine Subagenten), nur die letzten ~30 Tage (Claude Code raeumt aeltere
  Protokolle ab) — Wiederholungen rechtzeitig terminieren.
"""
import glob
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime

CAP = 300
CHAIN = {"idea", "idea-review", "task", "feature-fast", "feature-discover", "feature-plan",
         "impl-plan", "plan-review", "feature-start", "implement", "impl-review", "worker",
         "workflow-checkpoint", "archive"}
CMD = re.compile(r"<command-name>/?dtb[-:]([\w-]+)</command-name>")
ANY_CMD = re.compile(r"<command-name>/?([\w:-]+)</command-name>")
PH = ["P_start", "P0_verlust", "P1_sammeln", "P2_status_sync", "P3_log", "P4_status",
      "P4b_dashboard", "P5_abschluss", "Mensch"]
SKIP_TEXT = ("<", "[Request", "Caveat")
FRAGE_ARTEN = [
    ("Sammelvorlage/Kontrollpunkt", r"nicht gestrichenen|streiche \{|Verlustfunde erfassen|Kontrollpunkt —"),
    ("Alters-Vorlage", r"alle behalten"),
    ("Weiche Wechsel/Ende", r"Wechsel\W{1,3} oder"),
    ("Abnahme/Status-Frage", r"Fertig zum Testen|Abgenommen|Beleg|Abnahme"),
    ("Aufgaben-Zuordnung", r"ist .{0,60} = |dieselbe Aufgabe|gleiche Aufgabe|zuordnen"),
    ("Commit/Push danach", r"commit|Commit|push"),
    ("Merge/naechster Schritt", r"Merge|Soll ich|Moechtest du|Möchtest du|Willst du"),
]


def ts_of(e):
    try:
        return datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError, AttributeError):
        return None


def blob(inp):
    return json.dumps(inp, ensure_ascii=False).replace("\\\\", "/")


def classify(name, inp, cur):
    b = blob(inp)
    if name == "Skill":
        s = str(inp.get("skill", ""))
        if "no-loss-check" in s:
            return "P0_verlust"
        if "project-dashboard" in s:
            return "P4b_dashboard"
    if "dtb-no-loss-check" in b:
        return "P0_verlust"
    if "project-dashboard" in b:
        return "P4b_dashboard"
    if name in ("Write", "Edit"):
        if "lessons.md" in b or "INBOX-BEFUNDE" in b:
            return "P0_verlust"
        if "project-changelog" in b:
            return "P3_log"
        if "WORKFLOW_STATUS" in b:
            return "P4_status"
        if any(k in b for k in ("BACKLOG.md", "spec.md", "task.md", "ROADMAP", "INBOX.md")):
            return "P2_status_sync"
    if name in ("Read", "Grep", "Glob", "Bash"):
        if "project-changelog" in b and cur == "P3_log":
            return "P3_log"
        if "WORKFLOW_STATUS" in b or re.search(r"git (-C \S+ )?(status|log)", b):
            return cur if cur in ("P2_status_sync", "P3_log", "P4_status") else "P1_sammeln"
        if any(k in b for k in ("plan.md", "BACKLOG", "DERIVED_STATE", "spec.md")):
            early = ("P_start", "P0_verlust", "P1_sammeln", "P2_status_sync")
            return "P2_status_sync" if cur in early else cur
    return None


def is_core(name, inp):
    b = blob(inp)
    return name in ("Write", "Edit") and any(k in b for k in (
        "project-changelog", "WORKFLOW_STATUS", "project-dashboard.html", "lessons.md", "INBOX"))


def user_parts(e):
    content = (e.get("message") or {}).get("content")
    if isinstance(content, str):
        return [content], False
    items = [c for c in (content or []) if isinstance(c, dict)]
    texts = [c.get("text", "") for c in items if c.get("type") == "text"]
    return texts, any(c.get("type") == "tool_result" for c in items)


def segments(path):
    """Checkpoint-Segmente einer Sitzungsdatei: Liste von {file, start, args, events}."""
    evs = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = ts_of(e) if not e.get("isSidechain") else None
            if t:
                evs.append((t, e))
    segs, cur = [], None
    for t, e in evs:
        texts, has_tr = [], False
        if e.get("type") == "user":
            texts, has_tr = user_parts(e)
            joined = " ".join(texts)
            if ANY_CMD.search(joined) and not has_tr:
                if cur:
                    segs.append(cur)
                    cur = None
                dm = CMD.search(joined)
                if dm and dm.group(1) == "workflow-checkpoint":
                    cur = {"file": path, "start": t, "events": [], "args": joined}
                continue
        content = (e.get("message") or {}).get("content")
        if e.get("type") == "assistant" and isinstance(content, list) and cur:
            for c in content:
                if c.get("type") == "tool_use" and c.get("name") == "Skill":
                    short = str(c.get("input", {}).get("skill", "")).split(":")[-1].replace("dtb-", "")
                    if short in CHAIN and short != "workflow-checkpoint":
                        segs.append(cur)
                        cur = None
                        break
        if cur is not None:
            cur["events"].append((t, e, has_tr, texts))
    if cur:
        segs.append(cur)
    return segs


def analyse(seg):
    """Zeit je Phase, Kern, Rueckfragen und Antworten eines Segments."""
    phase, last_t, last_tool, last_txt = "P_start", seg["start"], None, ""
    acc, acc_core, timeline, answers = Counter(), Counter(), [], []
    core_end, asks, texts_n = None, 0, 0
    nlc = nlc_inline = False
    worktree, handoff_in = False, "WORKTREE-HANDOFF" in seg["args"]
    for t, e, has_tr, texts in seg["events"]:
        gap = min(max((t - last_t).total_seconds(), 0), CAP)
        last_t = t
        content = (e.get("message") or {}).get("content")
        bucket, has_text = None, False
        if e.get("type") == "user":
            body = " ".join(texts).strip()
            if has_tr and last_tool == "AskUserQuestion":
                bucket = "Mensch"
            elif body and not has_tr and not e.get("isMeta") and not body.startswith(SKIP_TEXT):
                bucket = "Mensch"
                texts_n += 1
                answers.append((gap, last_txt, body))
                if "WORKTREE-HANDOFF" in body:
                    handoff_in = True
        if e.get("type") == "assistant" and isinstance(content, list):
            for c in content:
                if c.get("type") == "text":
                    last_txt = c.get("text", "")
                    has_text = True
                    # nur der Guard-Abbruch markiert die Sende-Seite; die Kopfzeile des
                    # Hand-off-Blocks zitiert auch die Empfangsseite
                    if "⛔ dtb:workflow-checkpoint" in last_txt:
                        worktree = True
                    if re.search(r"Verlustpr\w+[^\n]{0,20}\d+ Fund", last_txt):
                        nlc_inline = True
                if c.get("type") != "tool_use":
                    continue
                name, inp = c.get("name"), c.get("input", {}) or {}
                last_tool = name
                asks += name == "AskUserQuestion"
                if name == "Skill" and "no-loss-check" in str(inp.get("skill", "")):
                    nlc = True
                p = classify(name, inp, phase)
                if p:
                    if phase in ("P4_status", "P4b_dashboard") and p == "P1_sammeln":
                        p = "P5_abschluss"
                    phase = p
                if is_core(name, inp):
                    core_end = t
        b = bucket or phase
        acc[b] += gap
        timeline.append((t, b, gap, has_text))
    if core_end:
        # Kern endet mit der ersten Modell-Nachricht mit Text nach dem letzten Kern-Schreibvorgang
        stop = next((t for t, _, _, txt in timeline if t > core_end and txt), core_end)
        for t, b, gap, _ in timeline:
            if t <= stop:
                acc_core[b] += gap
    kind = ("worktree" if worktree else "handoff" if handoff_in
            else "normal" if core_end else "ohne_kern")
    return {"date": seg["start"].date().isoformat(),
            "project": os.path.basename(os.path.dirname(seg["file"])),
            "total": sum(acc.values()) / 60,
            "core": sum(acc_core.values()) / 60 if core_end else None,
            "acc": acc_core if core_end else acc, "asks": asks, "texts": texts_n,
            "nlc": nlc, "nlc_inline": nlc_inline, "kind": kind, "answers": answers}


def frage_art(q):
    # die feste Weiter-Zeile des Checkpoints ist keine Commit-Frage
    q = "\n".join(l for l in q.splitlines() if not l.strip().startswith("→ Weiter mit:"))[-400:]
    for name, pat in FRAGE_ARTEN:
        if re.search(pat, q):
            return name
    return "sonstiges"


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    files = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    rows = sorted((analyse(s) for f in files for s in segments(f)), key=lambda r: r["date"])
    if not rows:
        print(f"0 Checkpoint-Segmente in {len(files)} Sitzungsdateien — nichts auszuwerten")
        return 0
    print(f"{len(rows)} Checkpoint-Segmente in {len(files)} Sitzungsdateien, "
          f"Zeitraum {rows[0]['date']} .. {rows[-1]['date']}")
    print("Arten:", dict(Counter(r["kind"] for r in rows)))
    norm = [r for r in rows if r["kind"] in ("normal", "handoff") and r["core"] is not None]
    if not norm:
        print("Keine normalen Laeufe mit Schreibvorgang — nichts auszuwerten")
        return 0
    med = statistics.median
    print(f"\nSegment-Median ueber alle: {med([r['total'] for r in rows]):.1f} min")
    print(f"Normal+Handoff: n={len(norm)}  Kern-Median {med([r['core'] for r in norm]):.1f} min, "
          f"Segment-Median {med([r['total'] for r in norm]):.1f} min, "
          f"Kern-Summe {sum(r['core'] for r in norm) / 60:.1f} h, "
          f"Segment-Summe {sum(r['total'] for r in norm) / 60:.1f} h")
    tot = sum(sum(r["acc"].values()) for r in norm) or 1
    print("\n| Phase | Median min | Mittel min | Anteil an Kern-Summe | Laeufe mit >0 |")
    print("|---|---|---|---|---|")
    for p in PH:
        vals = [r["acc"].get(p, 0) / 60 for r in norm]
        share = 100 * sum(r["acc"].get(p, 0) for r in norm) / tot
        print(f"| {p} | {med(vals):.1f} | {statistics.mean(vals):.1f} | {share:.0f} % "
              f"| {sum(v > 0 for v in vals)} |")
    n_skill = sum(r["nlc"] for r in norm)
    n_inline = sum((not r["nlc"]) and r["nlc_inline"] for r in norm)
    print(f"\nno-loss-check per Skill-Aufruf: {n_skill}/{len(norm)}; inline ohne Skill-Aufruf: "
          f"{n_inline}; ohne Spur: {len(norm) - n_skill - n_inline}")
    print(f"Auswahlfragen je Lauf: Mittel {statistics.mean([r['asks'] for r in norm]):.1f}; "
          f"Freitext-Antworten je Lauf: Mittel {statistics.mean([r['texts'] for r in norm]):.1f}")
    if "--rueckfragen" in argv or "--auszuege" in argv:
        agg = defaultdict(lambda: [0, 0.0])
        for r in norm:
            for gap, q, _ in r["answers"]:
                a = agg[frage_art(q)]
                a[0] += 1
                a[1] += gap
        wait = sum(v[1] for v in agg.values()) or 1
        print("\n| Rueckfrage-Art | Antworten | Wartezeit min | Anteil |")
        print("|---|---|---|---|")
        for k, (n, s) in sorted(agg.items(), key=lambda x: -x[1][1]):
            print(f"| {k} | {n} | {s / 60:.1f} | {100 * s / wait:.0f} % |")
    if "--auszuege" in argv:
        print("\n--- Auszuege (enthalten Personennamen — nicht weitergeben) ---")
        for r in norm:
            for gap, q, body in r["answers"]:
                q1 = q.strip().replace("\n", " / ")[-170:]
                print(f"{r['date']} {gap:4.0f}s | Q: {q1} || A: {body[:70]!r}")
    if "-v" in argv:
        print("\n| Datum | Projekt | Kern | Segment | " + " | ".join(PH) + " | Ask | nlc |")
        print("|---" * (len(PH) + 6) + "|")
        for r in norm:
            mark = "S" if r["nlc"] else ("I" if r["nlc_inline"] else "-")
            cells = " | ".join(f"{r['acc'].get(p, 0) / 60:.1f}" for p in PH)
            print(f"| {r['date']} | {r['project'][-28:]} | {r['core']:.1f} | {r['total']:.1f} "
                  f"| {cells} | {r['asks']} | {mark} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
