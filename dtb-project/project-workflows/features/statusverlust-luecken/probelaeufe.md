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

## 3.4 Vertraeglichkeit der Leser — 2026-09-23

**Pruefrage (L16):** Liest der Skill `## Offene Aufgaben` / `### Naechste Schritte` aus Status oder
Log — und stoeren `(seit …)`, `· behalten`, ⏳ oder `### Aufgaben-Abgaenge` seine Auswertung?
**Grep:** `grep -rn 'Offene Aufgaben\|Naechste Schritte' skills/` (13 Treffer ausserhalb des
Checkpoints) + alle `WORKFLOW_STATUS`-Leser.

| Skill | Befund |
|-------|--------|
| `backlog-status` (Z. 105), `feature-start` (Z. 65) | nicht betroffen — eigene Report-Ueberschrift aus `task.md`, liest die Liste nicht |
| `workflow-resume`, `workflow-status` | vertraeglich — lesen nur `## Handoff` bzw. „Laufende Arbeit" |
| `session-summary` | vertraeglich — fasst Logs frei zusammen; `erledigt: …` ist eindeutig lesbar |
| `workflow-next`, `project-health`, `impl-review` | vertraeglich — werten die Liste nicht aus (Status-Block, Log-Links, Artefakt-Liste) |
| `bug-report`, `debug-plan`, `docs-extract`, `feature-discover`, `feature-plan`, `generate-rules`, `impl-plan`, `project-init`, `task`, `workflow-next` (Z. 152) | nicht betroffen — `Naechste Schritte:` ist nur Ueberschrift der eigenen Chat-Ausgabe |
| `archive` (4e) | **angepasst** — loeschte „sonstige Referenzen" auf archivierte Items auch unter `## Offene Aufgaben` → Punkt ohne Abgangsvermerk weg (zweiter Schreiber an T2 vorbei). Jetzt: Zeilen dort bleiben, der naechste Checkpoint vermerkt den Abgang |

**Abweichung vom Plan:** `archive` stand nicht in der Dateiliste von 3.4 (Nutzerentscheid Option 1,
2026-09-23).

---

## 3.5 Probe-Checkpoint — 2026-09-23

**Aufbau:** Wegwerf-Projekt `probe-p3` im Scratchpad, kein Git. `WORKFLOW_STATUS.md`-Attrappe mit 5
Punkten (1 umformuliert, 2 zusammengelegt, 1 verworfen, 1 ueberfaellig ohne Session-Signal),
`session-verlauf.md` als Chat-Verlauf, Schwelle 7. Pruefer: unabhaengiger Subagent, read-only,
Repo-Fassung (T8). Erwartung VOR jedem Lauf festgehalten.

| Fall | Erwartung | Lauf 1 („ja, derselbe" · „passt") | Lauf 2 („nein, ersetzt" · unklar · „Abbruch") |
|------|-----------|--------|--------|
| Plan-Review umformuliert | `seit 2026-09-20` bleibt | ✓ (nach Zuordnungs-Rueckfrage, regelkonform) | ✓ `aufgegangen in …`, Nachfolger erbt 09-20 |
| README + CLAUDE.md zusammengelegt | 2× `aufgegangen in`, Ziel erbt 09-10 | ✓ | ✓ |
| CSV-Export verworfen | `verworfen` mit Grund | ✓ | ✓ |
| kit-sync ohne Signal | weitergetragen, keine Rueckfrage | ✓ | ✓ |
| ⏳ | genau EINE Vorlage: Doku (13 T) + kit-sync (22 T) | ✓ → `· behalten 2026-09-23` | ✓ unklar → 1 Rueckfrage → Abbruch → ⏳ bleibt, kein `behalten` |

**Lauf 1 → behoben (SKILL.md + Kanon §9):** E1 „ersetzt" hatte keinen Vermerk → Alter liess sich durch
Umformulieren + „nein" zuruecksetzen (jetzt `aufgegangen in`, erbt `seit`); E2 „sonst Rueckfrage" las sich
als Rueckfrage fuer jeden Punkt (jetzt: ohne Session-Signal still weitertragen); E3 ⏳ auf der NEUEN Liste,
nach den Zuordnungs-Rueckfragen; E5 Abbruch-Widerspruch („unveraendert" vs. ⏳) + Abbruch-Option in der
Vorlage; E6 Fallback fuer unklare Antworten; E9 Chat-Schritte ohne alten Punkt = neu; E12 §9.5
„Teil-Guard" → „Voll-Guard"; E13 Hand-off-Punkt-5-Bezug; E14 „Enter" gestrichen. Beispielausgabe (b)
an die neue Vorlagenzeile angeglichen.

**Lauf 2 → behoben:** D1 fester Wortlaut der ⏳-Rueckfrage; D2 Log-Momentaufnahme ohne Kontext/
`behalten`/⏳ jetzt auch im Kanon §9.1; D3 Vorrang „ersetzt" vor „neu" in Kopie und Kanon.

**Bewusst offen (nicht dieser Change / Ermessen):** E4 frisch zusammengelegter Punkt ist sofort ⏳-faellig
(gewollt: Umformulieren setzt das Alter nicht zurueck); E8 Kontext/Position des Zielpunkts beim
Zusammenlegen; E10 Git-Schritt ohne Nicht-Git-Fallback (Altbestand); E11 freie Gruende bei
„Verlustpruefung uebersprungen" (Altbestand); D4 wann eine Zuordnung „unsicher" ist (Ermessen, Ergebnis
gleich). **Zeilenbudget:** SKILL.md 470 → 510 (Grenze T5 exakt erreicht).

---

**Erstellt mit:** `/dtb:implement` (Schritte 2.5, 3.4, 3.5)
