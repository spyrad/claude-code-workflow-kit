# Discovery: Skill-Beschreibungen kürzen und abgrenzen
<!-- resume: done -->

**Erstellt:** 2026-11-26
**Idee-Referenz:** Inbox #217 — "Längengrenze für Skill-Beschreibungen (Auslöser)", darin zusammengelegt #218 "Vier Status-Skills in ihren Beschreibungen voneinander abgrenzen"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/CLAUDE.md` | Form-Regel für `description` (Template-Zeile :11, Feldbeschreibung :26) — bekommt die Längengrenze und die „Not for"-Regel |
| `skills/dtb-session-summary/SKILL.md` | `description` 1128 Zeichen → kürzen, `Use when:`-Präfix nachziehen |
| `skills/dtb-idea-rank/SKILL.md` | `description` 655 Zeichen → kürzen (Spalten-/Stufen-Details stehen im Body) |
| `skills/dtb-no-loss-check/SKILL.md` | `description` 543 Zeichen → kürzen, Proaktiv-Satz in Kurzform behalten |
| `skills/dtb-project-dashboard/SKILL.md` | `description` 358 Zeichen → kürzen + „Not for"-Satz |
| `skills/dtb-workflow-next/SKILL.md` | `description` 227 Zeichen → „Not for"-Satz |
| `skills/dtb-workflow-status/SKILL.md` | `description` 261 Zeichen → „Not for"-Satz |
| `skills/dtb-backlog-status/SKILL.md` | `description` 210 Zeichen → „Not for"-Satz |

---

## Anforderungen

### Scope
**Enthalten:**
- Regel in `skills/CLAUDE.md`: `description` vom Modell aufrufbarer Skills (`disable-model-invocation: false`) höchstens 350 Zeichen (Kit-Maß, kein Plattformlimit), gemessen am gefalteten Text (Zeilenumbrüche und Einrückung zählen als ein Leerzeichen)
- Form: `Use when:`-Phrasen (deutsch) + ein Satz Zweck (englisch) + bei Überschneidung mit einem Nachbarn ein `Not for … (that is dtb:X)`-Satz; Modus- und Ausgabe-Details gehören in den Body
- Kürzen der vier aufrufbaren Skills über 350 Zeichen: session-summary, idea-rank, no-loss-check, project-dashboard (no-loss-check und project-dashboard nannte die Idee nicht — gemessen und per Veto-Vorlage bestätigt 2026-11-26)
- Je ein „Not for"-Satz für workflow-next, workflow-status, backlog-status, project-dashboard

**Nicht enthalten:**
- Prüfskript und CI für Skill-Regeln (Inbox #214)
- Längenprüfung in `dtb:project-health` Check 8
- Freigabe von `idea`/`bug-report` für den Modellaufruf (Inbox #181 a)
- Gesperrte Skills über 350 Zeichen (11 Stück: worker 757 … feature-plan 356) — sie kosten keinen Session-Kontext

### Gewuenschtes Verhalten
- Die zehn Beschreibungen, die in jede Session jedes Zielprojekts geladen werden, sind kurz
- Fragt der Mensch „was steht an" / „wo steckt was" / „offene Features" / „Projektstand als Seite", wählt das Modell den passenden Status-Skill, weil jede Beschreibung ihre Nachbarn ausschließt
- Gemessene Ausgangslage (gefalteter Text): session-summary 1128, idea-rank 655, no-loss-check 543, project-dashboard 358, lesson 305, meeting-agenda 299, open-question 296, workflow-status 261, workflow-next 227, backlog-status 210

### Randfaelle
- Beim Kürzen darf kein Auslöse-Anlass verloren gehen — die Phrasen sind der eigentliche Auslöser. Wörtlicher Erhalt aller Phrasen passt bei session-summary nicht unter die Grenze (Phrasen allein rund 320 Zeichen); zusammengelegte oder gestrichene Phrasen werden deshalb aufgelistet und vom Menschen als abgedeckt bestätigt
- Der Proaktiv-Satz von no-loss-check ist ein Auslöser, kein Detail — er bleibt in Kurzform
- session-summary beginnt heute mit „Use when the user wants…" statt `Use when:` — Formverstoß, wird beim Kürzen behoben
- Die wegfallenden Details stehen bereits im Body: session-summary Modus-Tabelle (`skills/dtb-session-summary/SKILL.md:38-44`), idea-rank Spalten und Stufen (`skills/dtb-idea-rank/SKILL.md:135`, `:227`)

### Einschraenkungen
- Die Auslösung liest die installierten Kopien unter `~/.claude/skills/`, die erst nach Merge und `dtb:kit-sync` stehen — im Worktree ist nur die Repo-Fassung prüfbar
- Der „Not for"-Satz verweist nur auf existierende Skills

### Integrationspunkte
- `dtb:pipeline-graph` zeigt den vollständigen `description`-Text (`skills/dtb-pipeline-graph/SKILL.md:33`) — wird kürzer, bricht nicht
- `dtb:project-health` prüft nur die Existenz von `description` (`skills/dtb-project-health/SKILL.md:216`) — unberührt
- Inbox #214 kann die Regel später als Skript-Prüfung übernehmen

---

## Abhaengigkeiten

- Keine Konflikte. Ergänzt Inbox #214 (Skript-Ebene) und grenzt sich von #181 a (Freigabe statt Länge) ab.

---

## Offene Punkte

- Auslöse-Probe nach Merge und `dtb:kit-sync`: in einer frischen Session die vier Status-Fragen stellen und prüfen, ob der passende Skill gewählt wird

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-26)
