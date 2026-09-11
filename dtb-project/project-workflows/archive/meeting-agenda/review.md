# Review-Snapshot: meeting-agenda

Scope: skills/dtb-meeting-agenda/SKILL.md (neu), skills/dtb-open-question/SKILL.md,
skills/dtb-meeting-dump/SKILL.md, CLAUDE.md · Geprueft bis: `3730706` · Datum: 2026-08-02
Gesamt-Verdikt: REJECTED (Stand des Review-Laufs) — Triage 2026-08-02: 13 Fixed / 0 Skipped / 0 Pending

Achsen: Plan Adherence WARNING (1) · Scope Discipline PASS (0) · Safety & Quality FAIL (4) ·
Architecture FAIL (3) · Pattern Consistency WARNING (3) · Rules uebersprungen (keine Coding-Rules)

## Findings

### F1 — Safety & Quality — [S:Hoch × I:Hoch] — principled/blocking
skills/dtb-meeting-agenda/SKILL.md:56 (+ Frontmatter consumes) — Der Scan schliesst `plan.md` ein,
aber kein Kettenteilnehmer bedient diesen Ort: `open-question:103-108` bricht ausdruecklich ab
(„## Offene Punkte gehoert nicht in diese Dateien — MVP-Schnitt #13"), `meeting-dump:112-113`
scannt nur spec.md und discovery.md. Eine Frage in einem plan.md erschiene auf jeder Agenda und
koennte nie abgehakt werden (Dauer-Eintrag ohne Schliess-Pfad).
Fix: `plan.md` aus Schritt 4 und aus `consumes` streichen (symmetrisch zu meeting-dump).
Decision: FIXED

### F2 — Architecture — [S:Hoch × I:Mittel] — torvalds/blocking
skills/dtb-meeting-dump/SKILL.md:26-27 — Dieselbe Kette in drei Reihenfolgen: neue Frontmatter-Kante
(Agenda vor Dump), Fliesstext („Erfassung #26 → Rueckfluss #24 → Lese-Agenda #25"), CLAUDE.md
(„#13→#26→#25→#24"). Kante gesetzt, Satz daneben nicht mitgezogen.
Fix: Satz auf „… → Lese-Agenda (#25) → Rueckfluss (dieser Skill, #24)" umstellen.
Decision: FIXED

### F3 — Architecture — [S:Mittel × I:Hoch] — torvalds/non-blocking
skills/dtb-pipeline-graph/SKILL.md:188 — „Monitoring-Skills haben keine Kanten (standalone)"
widerspricht den zwei neuen Gegenkanten. Trifft die Annahme, auf der plan-review-Variante C beruhte.
Fix: praezisieren auf „Monitoring-Skills deklarieren selbst keine Kanten; Gegenkanten aus
Nachbar-Skills werden gezeichnet".
Decision: FIXED

### F4 — Plan Adherence — [S:Mittel × I:Mittel] — SHA-Vollstaendigkeits-Check
features/meeting-agenda/plan.md ## Progress 1.4 — Beleg `kit-sync @ 59b3e4e` kollidiert mit dem
Multi-Repo-Format `repo-name@SHA` (§2 Regel 5); ein Parser laese „kit-sync" als Repo-Namen.
Fix: auf `59b3e4e` kuerzen, Erklaerung in Klammern hinter die Backticks.
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Mittel] — principled/non-blocking
skills/dtb-meeting-agenda/SKILL.md:59-70 — Aufnahmekriterium schliesst Fliesstext-Doku aus, aber
nicht Code-Fences. Ein Beispielblock mit `## Offene Punkte` + Kanonzeilen in einer kuenftigen
spec.md erfuellt beide Bedingungen → Phantom-Fragen. §7.1 loest dieselbe Klasse bewusst.
Fix: dritte Ausschluss-Bedingung „Zeilen innerhalb eines Code-Fence" ergaenzen.
Decision: FIXED

### F6 — Pattern Consistency — [S:Mittel × I:Mittel] — principled/non-blocking
skills/dtb-meeting-agenda/SKILL.md:39-42 — „traegt keine eigene Format-Logik" ist faktisch falsch;
Schritt 4 spiegelt die §6-Grammatik, der Fallback-Pfad haengt davon ab. Der sonst uebliche Marker
„> **Wartungs-Hinweis (Format-Kopplung):**" fehlt.
Fix: Wartungs-Hinweis ergaenzen, Satz auf „spiegelt §6, Single Source bleibt die Regel-Datei"
korrigieren; meeting-agenda als fuenften Akteur in den bestehenden Kopplungs-Hinweisen nennen.
Decision: FIXED

### F7 — Pattern Consistency — [S:Mittel × I:Niedrig] — principled/non-blocking
skills/dtb-open-question/SKILL.md:166, skills/dtb-meeting-dump/SKILL.md:211 — Abschluss-Meldungen
verweisen auf `/dtb:workflow-next` „bzw. der geplanten Fach-Agenda". workflow-next ist nach §6.2
blind gegen `## Offene Punkte`, und die Agenda ist gebaut, nicht geplant.
Fix: in beiden Meldungen auf `/dtb:meeting-agenda` umstellen.
Decision: FIXED

### F8 — Safety & Quality — [S:Niedrig × I:Mittel] — principled/non-blocking
skills/dtb-meeting-agenda/SKILL.md:142-152 — Leer-Fall ist modus-unabhaengig formuliert; bei
0 offenen, aber vorhandenen beantworteten Fragen unterschlaegt `alle` das Angeforderte —
Widerspruch zur eigenen Regel zwei Absaetze darueber.
Fix: ergaenzen, dass im `alle`-Modus „Zuletzt geklaert" auch nach dem Leer-Block folgt.
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Mittel] — torvalds/non-blocking
skills/dtb-meeting-agenda/SKILL.md:93 — Reihenfolge DER Gruppen undefiniert; Glob liefert nach
Aenderungszeit → zwei Laeufe ergeben unterschiedlich sortierte Agenden. workflow-next:115-117
definiert seine Sortierung explizit.
Fix: „Gruppen alphabetisch nach Slug" ergaenzen.
Decision: FIXED

### F10 — Safety & Quality — [S:Niedrig × I:Niedrig] — principled/non-blocking
skills/dtb-meeting-agenda/SKILL.md:130-135 — „Zuletzt geklaert" ohne Sortierung und Obergrenze;
waechst monoton, Ueberschrift wird zur Falschaussage. Vorbild backlog-status:86 „(letzte 5)".
Fix: „absteigend nach Meeting-Datum, max. 5".
Decision: FIXED

### F11 — Safety & Quality — [S:Niedrig × I:Niedrig] — principled/nit
skills/dtb-meeting-agenda/SKILL.md:48 / :120 — „letzter Zwischenstand" nicht definiert: letzte
Zeile in Datei-Reihenfolge oder juengstes `(Meeting YYYY-MM-DD)`? Faellt auseinander, sobald ein
Meeting verspaetet nachbereitet wird (meeting-dump:64-65 erlaubt das). Der alle-Modus definiert
„Datei-Reihenfolge", der Standard-Modus nicht.
Fix: auf „die letzte `→ Zwischenstand:`-Zeile in Datei-Reihenfolge" praezisieren.
Decision: FIXED

### F12 — Pattern Consistency — [S:Niedrig × I:Niedrig] — principled/nit
dtb-project/project-rules/DERIVED_STATE_RULES.md:265-266 — §6.3 nennt den lesenden Konsumenten
weiterhin „eine kuenftige rein-lesende Agenda-Ansicht (#25, noch offen)". Der Skill referenziert
§6 als alleinigen Kanon — der Kanon kennt ihn nicht.
Fix: durch `dtb:meeting-agenda` ersetzen (Seed-Aenderung, Fusszeile mitfuehren — #22-Skew).
Decision: FIXED

### F13 — Safety & Quality — [S:Niedrig × I:Niedrig] — torvalds/nit
skills/dtb-meeting-agenda/SKILL.md:46-52 — Argument-Vergleich nicht case-definiert (`alle` vs.
`Alle`); Schritt 4 nimmt `- [x]`-Zeilen ins Aufnahmekriterium auf, der Standard-Filter „nur offene"
schlaegt nur implizit ueber das Ausgabe-Template durch.
Fix: Zeile ergaenzen „Argument case-insensitiv; `- [x]`-Treffer nur im `alle`-Modus ausgeben".
Decision: FIXED
