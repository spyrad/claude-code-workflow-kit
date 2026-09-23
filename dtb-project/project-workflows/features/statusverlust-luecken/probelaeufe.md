# Probelaeufe: Statusverlust-Luecken schliessen

**Zweck:** Ablageort (L20) fuer die Eigenpruefungen der Schritte 2.5, 3.5, 4.5, 4.6 — die
Session-Logs schreibt im Worktree nur der Orchestrator (Hand-off), hier bleibt der Beleg am Change.
Status-neutral (zaehlt nicht fuer die Ableitung).

---

## 2.5 Task-Lane-Absicherung — 2026-09-23

**Aufbau:** Wegwerf-Projekt im Scratchpad (`probe-p2`), INBOX-Attrappen #993-#999, OHNE
`DERIVED_STATE_RULES.md` (prueft die operativen Kopien). Pruefer: unabhaengiger Subagent, read-only,
Repo-Fassung der SKILL.md (T8). Erwartung VOR dem Lauf festgehalten.

| # | Fall | Erwartung | Lauf 1 | Lauf 2 |
|---|------|-----------|--------|--------|
| 999 | Task-Lane-Vermerk, kein Link | Change fehlt → `/dtb:task 999` | ✓ | ✓ |
| 998 | Link auf nicht existierende Spec | Change fehlt | ✓ (naechster Schritt uneinheitlich) | ✓ `/dtb:feature-discover 998` in allen Skills |
| 997 | Link auf `archive/bar/` | Archiv-Kandidat | ✓ | ✓ |
| 996 | Link auf existierende `task.md` | Archiv-Kandidat | ✓ | ✓ |
| 995 | Verworfen | Archiv-Kandidat | ✓ | ✓ |
| 994 | nur Discovery verlinkt | Change fehlt | ✓ (in next doppelt) | ✓ `/dtb:feature-plan qux`, eingefaltet |
| 993 | Offen | kein Kandidat | ✓ | ✓ |

**Kernregel:** in beiden Laeufen korrekt, auch ohne DSR (operative Kopien tragen).

**Lauf 1 → behoben:** U1 Archiv-Zaehler in project-health zaehlte „Change fehlt" mit (6 statt 3);
U2 ❌ statt ⚠ in der Report-Vorlage; U3/U4 naechster Schritt je Skill verschieden bzw. unbestimmbar
→ EINE deterministische Regelzeile; U6 Doppelzeile in next; U8/U9 archive-Vorlagen; U10 Link-Ort und
„mindestens ein"; U11/U12.

**Lauf 2 → behoben:** N1 Discovery-Hinweis nur in project-health (Kanon eingeschraenkt); N2
workflow-status Queue-Zeile „Inbox (Change fehlt)" + Einfalten; N3 idea-rank Vorbedingungen fuer
`archive/`-Link und „Change fehlt"; N4 toter `features/`-Link bei vorhandenem `archive/{slug}/` = belegt
(sonst Fehlalarm nach Teil-Archivierung); N5 „erster zutreffender Zweig gilt"; N6 Detailzeilen-Format
project-health; N7 Kurztitel in next definiert.

**Mechanisch verifiziert nach Lauf 2:** Regelzeile „Naechster Schritt …", Link-Zeile und Kernsatz je
6/6 wortgleich (Kanon + archive, project-health, workflow-next, workflow-status, idea-rank).

**Bewusst offen (nicht dieser Change):** U5 — `workflow-next`/`project-health` haben keine Regel fuer
eine ganz fehlende `DERIVED_STATE_RULES.md` (Altbestand); U7-Rest — Rang zwischen Feature-, Aufgaben-
und Bug-Pipeline in next (Altbestand); N8 — zwei aehnliche „Nichts zu archivieren"-Meldungen (je Fall
eindeutig).

---

**Erstellt mit:** `/dtb:implement` (Schritt 2.5)
