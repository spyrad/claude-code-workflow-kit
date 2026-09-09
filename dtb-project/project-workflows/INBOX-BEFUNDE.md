# Befund-Becken (maschinelle Verlustfunde)

> Automatisch erfasste Funde aus der Verlustpruefung (`dtb:no-loss-check` /
> `dtb:workflow-checkpoint` Schritt 0). **Kein Eintrag hier wird gearbeitet** — er muss erst
> mit `/dtb:idea-triage` befoerdert werden. Fach-Wuensche gehoeren nach `INBOX.md`, nicht hierher.

**Sichtung-Spalte:** leer = neu, noch nie gesichtet · `L1 YYYY-MM-DD` = einmal liegengelassen,
der naechste Lauf erzwingt die Entscheidung · `Altbestand` = aus der Migration uebernommen.

**„Ungesichtet" heisst: noch nicht endgueltig entschieden** — also `leer` ODER `L1 …` ODER
`Altbestand`. Diese eine Definition gilt fuer alle Zaehler (Handoff-Erinnerung des Checkpoints,
`dtb:project-health`, Abschluss-Bilanz der Triage). Entschieden ist ein Eintrag erst, wenn er das
Becken verlassen hat — durch Befoerderung oder Verwerfen.

**Nummernkreis:** gemeinsam mit `INBOX.md` — eine Nummer wird nie zweimal vergeben, und sie
bleibt bei der Befoerderung erhalten (Session-Logs referenzieren Nummern).

**Feld-Hygiene:** literale Pipes im Befund-Text escapen — sonst bricht die Zeile die Tabelle.

---

| # | Datum | Befund | Sichtung |
|---|-------|--------|----------|
| 77 | 2026-09-09 | **Neu geschriebene Konventionen vor dem Commit gegen den eigenen frisch gebauten Code gegenpruefen** — im Moment der Niederschrift liegt der Gegenbeleg am naechsten. Belegt 2026-09-08: die neue Zwei-Becken-Regel in `skills/CLAUDE.md` verlangte kategorisch, dass Abgleiche beide Dateien lesen, waehrend der im selben Zug gebaute `dtb:idea-triage` mit Begruendung nur eine liest (impl-review F4) |  |
| 78 | 2026-09-09 | **Haengen zwei Skills an derselben Bedingung, muss der Satz auf beiden Seiten WORTGLEICH stehen** — eine sinngemaess nachgezogene Bedingung laeuft beim naechsten Umbau auseinander. Belegt 2026-09-08: `no-loss-check` unterdrueckte seine Abschlussfrage bei nicht-leerer dringender Gruppe, der Checkpoint war laengst auf nicht-leere Vorlage umgestellt — im neuen Fall standen zwei Fragen uebereinander (impl-review F5, vergroesserte INBOX #73) |  |
| 79 | 2026-09-09 | **In Python-Skripten mit deutschem Text keine typografischen Anfuehrungszeichen in Doppelquote-Strings** — sie brechen das Literal; Backticks oder einfache Quotes verwenden. Belegt 2026-09-08: ein Triage-Fix-Skript scheiterte an einem SyntaxError, weil der Ersetzungstext deutsche Anfuehrungszeichen enthielt |  |
| 80 | 2026-09-09 | **Skripte mit repo-relativen Pfaden immer vom Repo-Root aus starten** — ein `cd` in einem frueheren Bash-Block verschiebt das Arbeitsverzeichnis der Folgeaufrufe. Belegt 2026-09-08 zweimal in einer Sitzung (FileNotFoundError auf `skills/...`) |  |
| 81 | 2026-09-09 | **Migration der 24 Altbestands-Befunde aus `INBOX.md` ins Becken** — Folgevorgang zu #76, bewusst aus dessen Scope ausgelagert. Zuordnungsvorschlag nach dem Beleg-Muster mit Veto je Nummer; Grenzfaelle #15 (Fach-Wunsch mit Beleg-Wort), #34 und #64 (Entscheidungsfragen, keine Befunde) gehoeren in die Haupt-INBOX. Ohne diesen Lauf bleibt die Haupt-INBOX bei 37 statt 13 Eintraegen |  |
| 82 | 2026-09-09 | **`dtb:kit-sync` Klassen-Tabelle: gehoert `agents/CLAUDE.md` wirklich in Klasse A?** Die Datei ist Autoren-Doku, wird aber ueber das Muster `agents/*.md` mitverteilt und drift-geprueft wie ein Artefakt. Aufgefallen 2026-09-08 beim Sync-Lauf (ein selbstgebauter Ausschluss meldete sie faelschlich als verwaist) |  |
