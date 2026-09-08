# Discovery: Checkpoint erfasst Verlustfunde
<!-- resume: done -->

**Erstellt:** 2026-09-08
**Idee-Referenz:** Inbox #72 — "`dtb:workflow-checkpoint` soll die Lektionen aus der Verlustpruefung selbst absetzen statt sie als Befehle zurueckzugeben."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-workflow-checkpoint/SKILL.md` | Wirkstelle: Schritt 0 ruft heute `dtb:no-loss-check` und reicht die Funde nur als Befehle weiter (373 Zeilen) |
| `skills/dtb-lesson/SKILL.md` | Referenzquelle: Schritt 2 Feld-Ableitung, Schritt 3 Duplikat-Check, Schritt 4 Append-only (213 Zeilen) |
| `skills/dtb-no-loss-check/SKILL.md` | Liefert die Funde in zwei Gruppen nach Verlustrisiko; Uebergabeformat ggf. betroffen (414 Zeilen) |
| `dtb-project/project-rules/lessons.md` | Zieldatei fuer Lektionen, seit 2026-09-07 versioniert (`f75979d`) |
| `skills/CLAUDE.md` | Konventionen: Spiegel-Kopplung, Schreibgrenzen, `disable-model-invocation`-Regel |
| `skills/dtb-feature-fast/SKILL.md` | Musterquelle fuer die vetobare Sammelvorlage |
| `skills/dtb-idea/SKILL.md` | Referenzquelle fuer Ideen-Funde (Duplikat-Check, Nummernvergabe) |
| `skills/dtb-pipeline-graph/SKILL.md`, `skills/dtb-project-health/SKILL.md` | Lesen Pipeline-Frontmatter; neue Kante muss beidseitig notiert werden (#46) |

**Zwei Scan-Befunde:**
- Die Uebergabedaten existieren bereits: `dtb:no-loss-check` schreibt vor, dass jede Befehlszeile ohne Nacharbeit absetzbar ist (ausformulierter Freitext). Der Checkpoint muss nichts neu strukturieren.
- Harter Constraint: `dtb:lesson` und `dtb:idea` tragen `disable-model-invocation: true`. Ein echter Aufruf aus dem Checkpoint ist gesperrt (Schritt 0 des Checkpoints begruendet den `no-loss-check`-Aufruf ausdruecklich mit dessen `false`). Wiederverwendung geht nur per Referenz auf die Schritte, oder das Flag wird gekippt (nimmt #69 vorweg).

---

## Anforderungen

### Scope
**Enthalten:**
- Funde der Gruppe **„Vor dem Checkpoint erledigen"** (Verlustrisiko-Gruppierung von `dtb:no-loss-check`) werden vom Checkpoint **automatisch erfasst** — beide Typen, Lektionen und Ideen
- Automatisch erfasste Eintraege tragen eine **Kennzeichnung**, dass sie ueber den Checkpoint kamen (Herkunfts-Marker im Zielartefakt, nicht per Hand abgesetzt)
- Die Schnittachse ist die Verlustrisiko-Gruppe, nicht der Typ (Lektion vs. Idee)

**Nicht enthalten:**
- Funde der Gruppe **„Kann warten"** — bleiben wie heute kopierfertige Befehle im Report, keine automatische Erfassung
- Aenderung an der Gruppierungslogik von `dtb:no-loss-check` selbst (siehe Offene Punkte)

**Datenlage zur Entscheidung (2026-09-08 aus den Session-Logs):** In allen drei Sessions, die die Gruppierung festhielten (08-14, 08-16 S1, 08-18), war die dringende Gruppe leer — 6/6 „Kann warten". Fuer 19 weitere Funde aus fuenf Sessions steht die Gruppe nicht im Log. Der Schnitt ist damit bewusst eng: er greift nur bei echtem Verlustrisiko.

### Gewuenschtes Verhalten
- **Sammelvorlage mit zeilenweisem Streichen** (Muster `dtb:feature-fast`): der Checkpoint zeigt alle dringenden Funde als EINE Vorlage, der Mensch bestaetigt einmal fuer alle oder streicht einzelne Zeilen
- **Eine Bestaetigung fuer alle** reicht — bei der typischen Groesse der dringenden Gruppe (1-3 Funde) keine Rueckfrage je Fund
- **Nie still:** die Schreibregel „Nie stiller Auto-Write" aus `dtb:lesson` bleibt eingehalten — die Vorlage IST die Bestaetigung. Verworfen: stilles Schreiben (verstoesst gegen die wiederverwendete Regel) und Einzel-Rueckfrage je Fund (der heutige Zustand, der zum Liegenbleiben fuehrt)
- Nach dem Schreiben meldet der Checkpoint, was erfasst wurde (Zielartefakt + Nummer/Kennung je Eintrag)

### Randfaelle
- **Dringende Gruppe leer:** Vorlage entfaellt still, kein leerer Block (nach Datenlage der haeufigste Fall)
- **Duplikat-Treffer:** Zeile in der Vorlage mit Fundstelle markieren (z.B. „aehnlich L23") und vorgestrichen zeigen — nicht hart blocken, wie `dtb:lesson` Schritt 3 es heute haelt
- **Alle Zeilen gestrichen:** nichts schreiben, eine Meldezeile, Checkpoint laeuft weiter
- **Schreibfehler mitten drin:** beide Ziele sind append-only, ein Teilzustand ist nicht kaputt — melden, was geschrieben wurde und was nicht; die Restbefehle wie heute ausgeben
- **Mehr als 10 dringende Funde:** keine ueberlange Vorlage — Rueckfall auf den heutigen Report mit Befehlen (Muster Selbst-Eskalation `dtb:feature-fast` 3.6)
- **Bewusst ausserhalb von #72:** Pipes im Fund-Text zerlegen die INBOX-Zeile (`dtb:idea` escapet nicht — #54/#70). Bleibt ein #70-Problem, die Vorlage escapet nicht
- **Bereits stromaufwaerts abgedeckt:** Worktree (Checkpoint hat Voll-Guard, laeuft nur im Orchestrator); Zweitlauf derselben Sitzung (`dtb:no-loss-check` Randfall 3 schliesst den vorigen Report als Quelle aus)

### Einschraenkungen
- **Schreiber-Regel (Entscheidung, #72 Punkt 1): Referenz, kein Aufruf.** `dtb:lesson` und `dtb:idea` bleiben auf `disable-model-invocation: true` — das Flag steuert nur das Starten eines Skills durch das Modell, nicht das Lesen einer Datei. Der Checkpoint liest `dtb-lesson/SKILL.md` (Schritte 2-4) und `dtb-idea/SKILL.md` (Duplikat-Check, Nummernvergabe, Format) und fuehrt die Schritte selbst aus; die Logik lebt weiter an genau einer Stelle. Praezedenz: `dtb:pane-start` → `dtb:worker` (ebenfalls `true`), Quelle aufgeloest ueber installierte Kopie `~/.claude/skills/`, Fallback Repo
- **Struktur-Check als Kopplungs-Waechter** (Muster `dtb:pane-start` → `## Struktur-Check`): Anker-Sektionen der Quellen vor dem Schreiben pruefen, zwei getrennte Fehlerpfade (Quelle fehlt = Installationsproblem; Anker fehlt = Drift → kein Schreiben auf veralteter Basis, Rueckfall auf Befehle im Report). Benanntes Restrisiko wie bei `pane-start`: der Check prueft Anker-Existenz, nicht Inhalt (F1-Klasse vom 2026-09-07)
- **Deklaration im Frontmatter, nicht im Flag:** `produces` des Checkpoints wird um `project-rules/lessons.md` und `INBOX.md` erweitert — die ehrliche Aussage „schreibt jetzt auch dorthin", zugleich die Pipeline-Kante fuer `pipeline-graph`/`project-health` (beidseitig notieren, #46)
- **Werkzeuge:** Checkpoint hat `Read, Write, Bash`; die referenzierten Schritte nutzen `Grep`/`Edit` — `Bash` deckt grep und append ab, kein Frontmatter-Eingriff
- **Marker darf keine Spalte hinzufuegen:** `lessons.md` 6 feste Spalten, INBOX 4; fuenf Skills lesen die Tabellen. Arbeitsannahme: Suffix im Textfeld `(via Checkpoint YYYY-MM-DD)` — in `Context` (lessons) bzw. im Idee-Text (INBOX)
- **Klasse A:** drei Skill-Dateien sind Klasse A — `kit-sync`-Nachlauf ist Teil des Abnahmekriteriums; die installierte Kopie ist die, die laeuft
- **Fachlich, per Referenz geerbt:** `lessons.md` append-only, INBOX-Nummer max+1, Datum `YYYY-MM-DD`, „Nie stiller Auto-Write" (die Vorlage ist die Bestaetigung)

### Integrationspunkte
- **`dtb:no-loss-check` → Checkpoint (Report-Format wird Kopplung):** die Skill-Kante ist beidseitig notiert (`next`/`after`). Neu liest der Checkpoint das Report-Format (Gruppen-Ueberschriften `## Vor dem Checkpoint erledigen` / `## Kann warten`, Befehlszeilen `→ /dtb:lesson "…"` / `→ /dtb:idea "…"`). `no-loss-check` traegt heute keinen Wartungs-Hinweis mit benanntem Leser → Wartungs-Hinweis (Format-Kopplung) ergaenzen, Leser Checkpoint (Kit-Muster wie `feature-discover` → `impl-plan`)
- **Checkpoint → `lessons.md` / `INBOX.md` (neue Datei-Kanten):** `produces` erweitern (3d). Keine Skill-Kante zu `lesson`/`idea`, weil kein Aufruf stattfindet
- **Checkpoint → Session-Log:** feste Log-Zeile in Teil 1 — Funde je Gruppe, davon erfasst mit Kennung (z.B. „2 dringend → L38, #73 erfasst · 5 kann warten, Befehle im Report"). Schliesst die Luecke, dass 5 von 8 Logs die Gruppierung nicht tragen
- **`dtb:idea-review` liest INBOX** (Spalten `#`, `Datum`, `Idee`): Suffix-Marker im Idee-Text bricht nichts. Nutzung des Markers fuer die Triage ist #33-Gebiet, nicht #72
- **Keine Aenderung:** `dtb:session-summary` (Abgrenzungstext bleibt wahr) und `dtb:workflow-status` (Tabellenzeile bleibt wahr). Keine externen Abhaengigkeiten

---

## Abhaengigkeiten

- **Bestehende Features (4):** keine Konflikte. `feature-fast` ist Musterquelle der Sammelvorlage, kein Konkurrent
- **INBOX #69** (Model-Invocation der Capture-Skills): loest dasselbe Problem von der anderen Seite — bleibt unabhaengig, #72 nimmt es nicht vorweg (Flag bleibt `true`, siehe Einschraenkungen)
- **INBOX #56, #52, #35:** fassen dieselbe Skill-Datei `dtb-workflow-checkpoint` an — Merge-Risiko bei Parallelarbeit, kein fachlicher Konflikt
- **INBOX #46, #58** (halbseitige Pipeline-Kanten): #72 fuegt zwei Datei-Kanten hinzu — beidseitig notieren
- **INBOX #33** (Triage-Sicht): koennte den Herkunfts-Marker nutzen — ausserhalb von #72
- **INBOX #70/#54** (Pipes in INBOX-Zeilen): bewusst ausserhalb von #72

---

## Offene Punkte

- Wendet `dtb:no-loss-check` die Regel „im Zweifel erste Gruppe" tatsaechlich an? Belegt sind 6/6 „Kann warten" — entweder ist fast alles rekonstruierbar, oder die Gruppierung ist zu locker. Aus den Logs nicht unterscheidbar; gehoert nicht in den Scope von #72
- 5 von 8 Session-Logs tragen die Gruppierung der Verlustfunde nicht — der Checkpoint schreibt sie heute nicht mit

---

**Erstellt mit:** `/dtb:feature-discover`
