# Discovery: Lektionen kuratieren
<!-- resume: done -->

**Erstellt:** 2026-10-27
**Idee-Referenz:** Inbox #141 — "Lektionen kuratieren: ein Lauf (Vorbild Vorsortierung #137) prüft lessons.md auf überholt / doppelt / schon in skills/CLAUDE.md gehoben und schlägt per Sammelliste vor; Aussortiertes wandert mit Grund nach archive/lessons-ausgemustert.md statt gelöscht zu werden (löst den Widerspruch append-only ↔ aussortieren); Auslöser die bestehende 150-Zeilen-Warnung"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-lesson-curate/SKILL.md | Neubau: der Kuratier-Skill (Name-Vorschlag, final in der Spec) |
| dtb-project/project-workflows/archive/lessons-ausgemustert.md | Neubau: Ablage ausgemusterter Lektionen mit Grund (append-only, Vorbild `INBOX-BEFUNDE-verworfen.md`) |
| dtb-project/project-rules/lessons.md | Kopftext „append-only … Kuratierung geschieht bewusst" + Soft-Limit; Ziel der Entnahme |
| skills/dtb-lesson/SKILL.md | Kopftext im Anlage-Template, Groessen-Warnung (Z. 204), Hebe-Hinweis `Applies-to: alle` (Z. 212) — sollen auf den neuen Skill zeigen |
| skills/dtb-idea-triage/SKILL.md | Vorbild: Hintergrund-Agenten in Portionen, Belegpflicht, Sammelliste mit Veto, Einzelfaelle mit Kappung, Werkzeug-Fehlschlag (3c); 4c prueft Funde gegen den Lektionen-Bestand |
| skills/CLAUDE.md | Pruefquelle „schon gehoben"; Worktree-Guard-Tabelle (Z. 469); Erfassungs-/Sammlungs-Kanon (Z. 130); Rueckfragen-Defaults |
| skills/dtb-workflow-checkpoint/SKILL.md | Schreibt Lektionen; Kandidat fuer Hinweis-Zeile ab Schwelle (analog `becken_schwelle`) |
| skills/dtb-project-dashboard/SKILL.md | Kennzahl Lektionen `{Zeilen}/150 Zeilen` (Z. 88) |
| skills/dtb-impl-plan/SKILL.md | Prior-Leser `lessons.md` — `L{N}`-Verweise nach Ausmusterung |
| skills/dtb-debug-plan/SKILL.md | Prior-Leser `lessons.md` |
| skills/dtb-plan-review/SKILL.md | Prior-Leser `lessons.md` |
| skills/dtb-impl-review/SKILL.md | Prior-Leser `lessons.md` |
| skills/dtb-implement/SKILL.md | Prior-Leser `lessons.md` |
| skills/dtb-feature-fast/SKILL.md | Prior-Leser `lessons.md` |
| skills/dtb-no-loss-check/SKILL.md | Duplikat-Pruefung neuer Funde gegen den Lektionen-Bestand |
| workflow.config.yaml | Moeglicher Schwellen-/Kappungs-Schluessel (analog `idea_triage:`) |
| CLAUDE.md | Skill-Liste (Knowledge management), Output Locations |
| README.md | Skill-Liste |
| dtb-project/project-workflows/archive/ARCHIVE_LOG.md | Nur Abgleich — Change-Format, nicht fuer Lektionen |

**Scan-Beobachtungen:**
- `lessons.md` hat 96 Zeilen, aber 56 KB (Lektion = eine lange Tabellenzeile) — die 150-Zeilen-Schwelle schlaegt nie an, obwohl jeder Prior-Leser ~14k Tokens laedt.
- L22–L34 fehlen: beim Versionieren 2026-09-07 (`f75979d`) nie eingecheckt (Zwei-Maschinen-Divergenz #64); archivierte Plaene verweisen auf L23, L25–L30.
- Reihenfolge nicht monoton (8 vor 7, 17→12 absteigend) — nach Nummer arbeiten, nicht nach Zeilenposition.

---

## Anforderungen

### Scope
**Enthalten:**
- Ein Lauf prueft jede Lektion gegen drei Ausmusterungs-Gruende:
  - **ueberholt** — die beschriebene Mechanik gibt es nicht mehr, oder ein Skill erzwingt die Regel inzwischen selbst
  - **doppelt** — eine andere Lektion ersetzt sie ohne Informationsverlust (Ersetzungsprobe, L10)
  - **schon gehoben** — die Regel steht bereits versioniert in `skills/CLAUDE.md` bzw. einer Projekt-Regeldatei
- Jeder Vorschlag mit pruefbarem Beleg (`datei:zeile`)
- Der Mensch bestaetigt EINE vorbefuellte Sammelliste mit Veto; unklare Faelle einzeln, gekappt pro Lauf
- Ausgemusterte Zeilen wandern samt Grund und Datum nach `archive/lessons-ausgemustert.md`; die Nummer bleibt erhalten und wird nie neu vergeben
- Der Widerspruch append-only ↔ aussortieren wird im Kopftext aufgeloest: append-only gilt fuer das Schreiben, Entnahme nur ueber diesen Skill
- Die Groessen-Warnung wird repariert (Bytes bzw. Lektionen-Anzahl statt Zeilen) und verweist auf den Skill

**Nicht enthalten:**
- Lektionen umformulieren, zusammenfuehren oder kuerzen — nur ganz ausmustern oder behalten
- Regeln selbst nach `skills/CLAUDE.md` heben — der Skill erkennt „schon gehoben", das Heben bleibt beim Menschen bzw. bei `dtb:lesson`
- Wiederherstellung der fehlenden L22–L34 (eigenes Thema)
- Automatisches Anspringen — nur vom Menschen gestartet

### Gewuenschtes Verhalten
- **Voller Bestand je Lauf** (kein Lesestand): Lektionen veralten durch spaetere Skill-Aenderungen, nicht durch ihr Alter — auch L1 kann morgen „gehoben" sein. Lauf ist selten (vom Menschen auf die Warnung hin gestartet), ~6 Portionen a 15 bei ~87 Lektionen
- Read-only Hintergrund-Agenten pruefen in Portionen (inline bei wenigen Lektionen); je Lektion Urteil `behalten` / `ueberholt` / `doppelt zu L{M}` / `gehoben → datei:zeile` mit Beleg und Sicherheit (hoch/mittel/niedrig)
- Uebersicht vor der Vorlage: Bestand, Vorschlaege je Grund, erwartete Einsparung (KB)
- **EINE Sammelliste** nur mit Sicherheit `hoch` + Beleg; der Mensch streicht per Nummer (Veto-Form)
- **`doppelt` in der Sammelliste nur bei einseitiger Ersetzung** (Agent nennt die bleibende Lektion, sie deckt die andere vollstaendig ab); Teilueberlappung oder offene Frage „wer bleibt" → Einzelfall
- **Im Zweifel behalten:** `mittel` → einzeln, gekappt per `einzeln_pro_lauf`; `niedrig` zaehlt als `behalten` (nur Zahl in der Bilanz). Asymmetrie wie L10 — zu Unrecht behalten kostet Tokens, zu Unrecht ausgemustert wiederholt einen Fehler
- `behalten` wird nicht vorgelegt
- **Sofortiges Schreiben je bestaetigter Entscheidung** (wie idea-triage): erst Archiv, dann Entnahme aus `lessons.md` — ein Abbruch verliert nichts und hinterlaesst nie eine Zeile an beiden Orten
- Abschluss-Bilanz: Ausgemustertes mit Grund, neuer Umfang (Zeilen/KB), Hebe-Hinweis fuer `Applies-to: alle`-Lektionen (nur Hinweis, kein Heben)
- Uebernommene Muster: idea-triage (Portionen, Belegpflicht, Sicherheitsstufen, Kappung, Werkzeug-Fehlschlag ≠ Datenbefund L7); Verworfen-Archiv `archive/INBOX-BEFUNDE-verworfen.md` (Spalten `#`, Datum, Grund)

### Randfaelle
**Fehler**
- Agent faellt aus oder liefert leer → Werkzeug-Fehlschlag, kein Datenbefund (L7): Lektionen der Portion gelten als `nicht geprueft → behalten`, Bilanz meldet sie; fallen alle Agenten aus → Abbruch ohne Schreiben
- Archiv geschrieben, Entnahme gescheitert → Lektion steht an beiden Orten; der naechste Lauf prueft zuerst auf Nummern in beiden Dateien, meldet sie und holt die Entnahme nach (kein doppeltes Archivieren)
- Entnahme ausschliesslich per `Edit` mit der exakten Zeile als Anker, nie per `Write` — eine parallel geschriebene neue Lektion bleibt unberuehrt

**Leere Daten / Grenzwerte**
- `lessons.md` fehlt oder hat keine Datenzeilen → Meldung, Ende
- Bestand unter der Warnschwelle → Lauf laeuft trotzdem (bewusst gestartet), eine Zeile meldet den Stand
- Archiv fehlt → Selbstanlage mit Kopf beim ersten Schreiben
- Zeilen, die nicht dem Muster `| N |` folgen, werden nie angefasst

**Edge Cases**
- **Nummernvergabe:** `dtb:lesson` vergibt heute „naechste laufende Nummer" aus `lessons.md` — wird die hoechste Nummer ausgemustert, entstuende ein Duplikat. Kuenftig Maximum ueber `lessons.md` + Archiv. Aendert nur `dtb:lesson` Schritt 4; Checkpoint und idea-triage nutzen ihn per Referenz und ziehen automatisch mit
- **Ketten bei `doppelt`:** die bleibende Lektion eines Paares ist im selben Lauf fuer Ausmusterung gesperrt; ist sie selbst Kandidat → Paar wird Einzelfall; Kreise (A↔B) → Einzelfall
- **`L{N}`-Verweise in offenen Changes** (z.B. „Wirklauf (L14/L29)") → Hinweis „referenziert in features/x" in der Sammelliste, nicht blockierend; Verweis bleibt ueber das Archiv aufloesbar
- **Hebe-Ziel fuer `gehoben`:** Kit-Repo `skills/CLAUDE.md`, Zielprojekte `{rules}/*.md` ohne `lessons.md` und `DERIVED_STATE_RULES.md` — beide pruefen, sofern vorhanden
- **Abwesenheits-Beleg fuer `ueberholt`:** Negativ-Grep mit Begriff und Suchraum („`X` → 0 Treffer in `skills/`") PLUS Stelle der Nachfolge-Mechanik; ohne Nachfolge-Stelle hoechstens Sicherheit `mittel`
- Nicht-monotone Reihenfolge → nach Nummer arbeiten, per Zeilen-Anker entnehmen, nie nach Position

### Einschraenkungen
**Technisch**
- **Voll-Guard:** `lessons.md` und `archive/` sind global geteilt (`skills/CLAUDE.md:432`) — Skill laeuft nur im Haupt-Checkout, bricht im verlinkten Worktree vor dem ersten Schreiben ab; Eintrag in die Guard-Tabelle (`skills/CLAUDE.md:469`)
- `disable-model-invocation: true` — nur vom Menschen gestartet
- **Groessen-Mass in KB statt Zeilen:** Prior-Kosten sind Tokens ≈ Bytes. Neuer Config-Block `lessons:` mit `schwelle_kb: 40` (Default) und `einzeln_pro_lauf: 5` — eigener Block, nicht `idea_triage.einzeln_pro_lauf` mitnutzen (zwei Skills, zwei Stellschrauben). Folge: bei heute 56 KB schlaegt die Warnung sofort an — gewollt
- Messung per `wc -c`; Werkzeug-Ausfall ist kein Befund (L7) → Warnung entfaellt mit Hinweiszeile
- **Eigenstaendiger Skill**, angelehnt an idea-triage, ohne Abschnitte per Referenz (deren Sektionen sind becken-spezifisch; Struktur-Checks ohne Gewinn). Ob die Zeilenform von `dtb:lesson` fuer das Archiv-Format per Referenz uebernommen wird, entscheidet impl-plan
- Klasse-A-Artefakt (`skills/dtb-*/SKILL.md`) → `kit-sync` verteilt automatisch

**Fachlich**
- **Nichts geht verloren:** Ausmustern = verschieben, nie loeschen. Archiv ist nicht ignoriert → versioniert wie `lessons.md` seit 2026-09-07; Git-Historie und Archiv sind zwei unabhaengige Rueckwege
- Ausgemusterte Lektionen sind kein Prior mehr — die Prior-Leser lesen das Archiv bewusst nicht
- Jede Ausmusterung bestaetigt der Mensch; ohne Bestaetigung wird nichts geschrieben, auch bei Sicherheit `hoch`

### Integrationspunkte
**Betroffene Features/Module**
- **`dtb:lesson` Schritt 4:** Nummernvergabe = Maximum ueber `lessons.md` + Archiv; Groessen-Warnung in KB gegen `lessons.schwelle_kb` mit Verweis auf den neuen Skill; Kopftext-Template (append-only gilt fuers Schreiben, Entnahme nur ueber den Skill)
- **Warnung an genau EINER Stelle** (`dtb:lesson` Schritt 4) — Checkpoint und idea-triage fuehren den Schritt per Referenz aus und erben sie; kein eigener Checkpoint-Hinweis analog `becken_schwelle` (waere ein zweiter Spiegel). impl-plan prueft, ob die Referenz die Unter-Sektion „Groessen-Warnung" mit ausfuehrt
- **`lessons.md` (Live-Datei):** Kopftext einmalig angleichen, dabei veraltete Leser-Liste korrigieren („code-review" → impl-review, `implement` ergaenzen)
- **`dtb:project-dashboard`:** Zusatzzeile Kennzahl Lektionen `{KB}/{schwelle_kb} KB` statt `/150 Zeilen`
- **Prior-Leser** (impl-plan, debug-plan, plan-review, impl-review, implement, feature-fast): keine Aenderung — lesen weiter nur `lessons.md`
- **Duplikat-Pruefer** (`dtb:lesson` Schritt 3, no-loss-check, idea-triage 4c): keine Aenderung — nur aktiver Bestand; eine neu erfasste ausgemusterte Lektion faengt der naechste Kuratier-Lauf wieder. Das Archiv ist Ablage, kein Vergleichsbestand
- **`workflow.config.yaml`:** neuer Block `lessons:` (`schwelle_kb`, `einzeln_pro_lauf`); ob das Config-Template in `dtb:project-init` mitzieht, prueft impl-plan
- **`skills/CLAUDE.md`:** Voll-Guard-Tabelle (Z. 469), Liste schreibender Skills (Z. 443), Rueckfragen-Defaults-Eintrag (Sammelliste/Einzelfaelle)
- **`CLAUDE.md`, `README.md`:** Skill-Liste (Knowledge management), Output Location `archive/lessons-ausgemustert.md`
- **Pipeline-Frontmatter** des neuen Skills (`stage`, `after`, `next`, `consumes`, `produces`) — `pipeline-graph`/`workflow-status` lesen automatisch

**Externe Abhaengigkeiten:** keine (lokale Dateien, Grep/Glob, Hintergrund-Agenten)

---

## Abhaengigkeiten

- Keine Konflikte mit bestehenden Change-Ordnern (dieser Branch traegt nur `lektionen-kuratieren`)
- **Ueberschneidung (parallel):** Worktree `feature/dashboard-projektname-hintergrund` aendert ebenfalls `skills/dtb-project-dashboard/SKILL.md` — NICHT die Lektionen-Kennzahl (Diff-Grep auf `Lektion|lessons|150` ohne Treffer, 2026-10-27). Gleiche Datei, andere Stelle → beim spaeteren Merge auf Textkonflikt achten; wer zuerst gemergt wird, ist egal
- Config-Punkt (Nachtrag 3e): `lessons:`-Block mit Default-Rueckfall im Skill; das `project-init`-Template traegt heute nur `status:` (nicht `idea_triage:`/`worker:`/`dashboard:`) — Aufnahme ins Template entscheidet impl-plan

---

## Offene Punkte

- Skill-Name final in der Spec festlegen (Vorschlag `dtb:lesson-curate`; Slug bleibt `lektionen-kuratieren`, passend zu Branch/Worktree)
- Fuehren Checkpoint (Schritt 0) und idea-triage (7f) bei ihrer Referenz auf `dtb:lesson` Schritt 4 die Unter-Sektion „Groessen-Warnung" mit aus? Sonst erbt die KB-Warnung nicht — impl-plan prueft
- Archiv-Format: Spalten der Lektion uebernehmen plus `Ausgemustert am` / `Grund` / `Beleg`? — impl-plan entscheidet (Vorbild `INBOX-BEFUNDE-verworfen.md`)
- `lessons:`-Block ins `project-init`-Config-Template aufnehmen oder nur Default-Rueckfall? — impl-plan
- Default `schwelle_kb: 40` am ersten echten Lauf gegenpruefen (heute 56 KB)
- Ausserhalb des Scopes: die fehlenden L22–L34 (beim Versionieren 2026-09-07 nie eingecheckt) — Kandidat fuer eine eigene INBOX-Idee, ueber den Hand-off an den Orchestrator

---

**Erstellt mit:** `/dtb:feature-discover`
