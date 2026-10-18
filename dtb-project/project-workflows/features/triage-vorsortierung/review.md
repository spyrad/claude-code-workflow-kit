# Review-Snapshot: triage-vorsortierung
Scope: skills/dtb-idea-triage/SKILL.md, workflow.config.yaml, CLAUDE.md, DERIVED_STATE_RULES.md, skills/CLAUDE.md, skills/dtb-{idea,idea-rank,lesson,open-question}/SKILL.md, probelauf-{testprojekt,becken}.md · Geprueft bis: `604e06d` · Datum: 2026-10-16
Gesamt-Verdikt: REJECTED

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | FAIL |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Architecture — [S:Hoch × I:Hoch]
skills/dtb-idea-triage/SKILL.md:346-358 — 4b bildet Buendel als transitive Huelle der `Verwandt`-Kanten; im Trockenlauf verschmolzen 5 Themen zu B3 (#132 + 20 Glieder). „Alle uebernehmen" erzeugt eine Idee fuer fuenf Changes, Streichen schickt 21 ungekappte Einzelfaelle nach Stufe 2.
Fix: Nur gegenseitige Kanten zaehlen; Buendel = Traeger + direkte gegenseitige Nachbarn, keine Huelle; uebrige Kanten bleiben „verwandt"-Hinweis.
Decision: FIXED (Simulation am Trockenlauf: 13 Buendel, groesstes 4 Funde, deckt die Probelauf-Themen)

### F2 — Safety & Quality — [S:Hoch × I:Mittel]
skills/dtb-idea-triage/SKILL.md:264-267 — Zeilenzahl-Gate zaehlt nur `#`-Zeilen, prueft nicht die Nummernmenge: eine fremde Nummer laesst die eigene still verschwinden und erzeugt zwei Vorschlaege fuer einen Fund.
Fix: Gate auf Mengengleichheit (jede Portionsnummer genau einmal, keine fremde), sonst Ausfall der Portion.
Decision: FIXED

### F3 — Plan Adherence — [S:Mittel × I:Hoch]
skills/dtb-idea-triage/SKILL.md Schritt 1 (Becken-Kopf, Satz „Entschieden ist ein Eintrag erst … durch Befoerderung oder Verwerfen") — neue Abgaenge fehlen; Sweep-Pruefprotokoll aus 3.3 fehlt im Commit-Text (L20).
Fix: Kopfsatz um Buendel/Nachtrag/Lektion/Fachfrage ergaenzen; Sweep-Liste in diesem Snapshot nachtragen.
Decision: FIXED

### F4 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:383-389, 461-463 vs. 736-738 — Kappung gilt nicht fuer von Schritt 7 verschobene Zeilen und aufgeloeste Buendel.
Fix: Kappung auf alle nicht vom Menschen herausgenommenen Zugaenge zu Schritt 6; Ausnahme (gestrichen / einzeln durchgehen) in „Wichtig" benennen.
Decision: FIXED

### F5 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:480-483 vs. 333-336 — Stufe 2 bietet Nachtrag/Lektion/Fachfrage nicht an; gestrichene Zeilen verlieren ihren Ausgang.
Fix: Option „0. Vorschlag uebernehmen ({Vorschlag})" bei Nachtrag/Lektion/Fachfrage mit gruener Quelle; Ausfuehrung ueber 7e/7f/7g.
Decision: FIXED

### F6 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:235, 370-377 — `Verwerfen: Dublette #M` mit #M in der Sichtungsmenge: zwei Funde koennen sich gegenseitig verwerfen.
Fix: In 4d `Dublette #M` mit #M in der Sichtungsmenge immer Einzelfall.
Decision: FIXED

### F7 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-idea-triage/SKILL.md:138-150, 516-518 — nach Fremdaenderung wird nicht geprueft, ob Zeile #N noch existiert; „Ziel vor Quelle" schriebe ein Ziel fuer einen Fund ausserhalb des Beckens.
Fix: Vor jedem Schreiben #N mit unveraendertem Text pruefen, sonst `⚠ #{N} nicht mehr im Becken — uebersprungen`.
Decision: FIXED

### F8 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-idea-triage/SKILL.md:391-400, 418 — keine Summenprobe in 4f; `{S}` doppeldeutig (4f vs. Kopf Schritt 5); `{G}` mit/ohne Traeger offen.
Fix: G = Glieder inkl. Traeger, S = Einzelzeilen ohne Buendel; `G + S + E + R = N` als hartes Gate; Kopf Schritt 5 auf dieselben Groessen.
Decision: FIXED

### F9 — Safety & Quality — [S:Mittel × I:Niedrig]
skills/dtb-idea-triage/SKILL.md:362-366 vs. 373-375 — 4c uebernimmt die Sicherheit auf eine neue (unscharfe) Dubletten-Behauptung; Beleg `lessons.md L{N}` ist kein Datei:Zeile.
Fix: 4c setzt `Sicherheit mittel`, Beleg `lessons.md:{Zeile} (L{N})`.
Decision: FIXED

### F10 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-idea-triage/SKILL.md:550-551 — 7a fuegt unter der Trennzeile ein; befoerderte Becken-Nummern liegen fast immer unter dem INBOX-Maximum, die absteigende Sortierung bricht.
Fix: An der sortierten Position einfuegen (vor der ersten Zeile mit kleinerer Nummer).
Decision: FIXED

Unterhalb des Caps (7): 7d vs. 7e uneinheitlich · „streichen" mit drei Bedeutungen (checkpoint/impl-review/triage) · doppelter bzw. zweiter Fachfrage-Vorsatz (A3, no-loss-check nutzt `[Fach-Frage ohne Ablage-Ort]`) · tote Zweige (Leer-Meldung „davon 0 neu", 4b.4, idea-Bedingung in 4a) · idea-triage fehlt in Voll-Guard-Tabelle und Lesestand-Spiegelliste in skills/CLAUDE.md · gefallene `dtb:idea` fail-open statt Stufe 2 (Drift 2.3, begruendet) · Nummern-Wiedervergabe nach Abgang des hoechsten Funds (aelter als das Feature).

## Triage 2026-10-16

10 Fixed · 0 Lesson · 0 Skipped (F1, F2 einzeln; F3–F10 als Sammelliste „Alle uebernehmen"). Fixes im Working Tree, nicht committet.

- F1: 4b neu — nur gegenseitige Kanten, Traeger + direkte Nachbarn, keine Huelle. Simulation am Trockenlauf-Ergebnis: 13 Buendel, groesstes 4 Funde (Handoff #132/#86/#118/#121, archive #130/#87/#94/#129, pane-start #126/#89/#115/#124, Hand-off-Empfang #131/#123/#128, Tick #127/#104/#116, feature-discover #47/#18/#32, Pfleger #53/#52; kit-sync in drei Paare)
- F3: Becken-Kopf (Schritt 1) nennt alle Abgaenge. Hinweis: das bestehende Kit-Becken `INBOX-BEFUNDE.md` traegt den alten Kopfsatz weiter — Datendatei, Nachzug nur durch den Orchestrator (Schreibgrenze), kein Laufzeit-Effekt
- F4: Kappung gilt gemeinsam fuer 4d-Einzelfaelle und von Schritt 7 verschobene Zeilen; ungekappt nur Herausgenommenes (4e, Schritt 6, Wichtig)
- F5: Stufe 2 Option 0 „Vorschlag uebernehmen" fuer Nachtrag/Lektion/Fachfrage; Zwangsentscheidung `L1` erlaubt 0/1/2
- F6–F10: wie im Finding; F8 legt `{G}` = Glieder **ohne** Traeger fest (gleiche Bedeutung wie `Gebuendelt` in der Bilanz, L47) und macht `{B}+{G}+{S}+{E}+{R}={N}` zum harten Gate
- Gegenprobe der Beschreibungen (L16, Pruefrage „traegt die Aussage nach dem Fix noch?"): nachgezogen `skills/dtb-idea/SKILL.md:142-145` (Einfuegeposition der Triage), `skills/CLAUDE.md` Zeile F (Dublette im selben Lauf), Root-`CLAUDE.md` (Buendel ohne Huelle, Dublette, Kappungs-Ausnahme, Option „uebernehmen")
- Automated-Kriterien der Phasen 1–3 nach der Triage erneut ausgefuehrt (L13): 15/15 gruen

### Sweep-Pruefprotokoll zu Plan 3.3 (nachgetragen, F3)

Pruefrage: „Zitiert die Fundstelle Schritt-Nummern oder Verhalten der Triage, und traegt die Aussage nach dem Umbau noch?" Grep `idea-triage` ueber `skills/`, `CLAUDE.md`, `DERIVED_STATE_RULES.md` (ohne den Skill selbst):

| Fundstelle | Ergebnis |
|------------|----------|
| `skills/CLAUDE.md:145, 187, 349, 372-375, 382, 387` | in p3 geaendert (Duplikat-Schutz, Kurzform, Zeile F, Zwei-Becken-Regel) — traegt |
| `skills/dtb-idea/SKILL.md:84` | in p3 geaendert (Kopplungs-Hinweis) — traegt |
| `skills/dtb-idea/SKILL.md:142-145` | **traegt nicht mehr nach F10** → in der Triage nachgezogen |
| `skills/dtb-idea-rank/SKILL.md:9, 340` | nennt nur den Gegenstand (Becken) — traegt, unveraendert |
| `skills/dtb-idea-rank/SKILL.md:41` | in p3 geaendert (Verhaltensbeschreibung) — traegt |
| `skills/dtb-idea-review/SKILL.md:11` | Frontmatter-Kante `after` — traegt, unveraendert |
| `skills/dtb-lesson/SKILL.md:96, 112, 157-158, 176` | in p3 geaendert; 157 („Treffer wird zum Verwerfen-Vorschlag") traegt auch nach F9 |
| `skills/dtb-open-question/SKILL.md:32, 107-110, 132-135, 166-168` | in p3 geaendert — traegt |
| `skills/dtb-project-init/SKILL.md:135` | Selbstanlage des Beckens — traegt, unveraendert |
| `skills/dtb-workflow-checkpoint/SKILL.md:12, 256, 304-336, 372` | Kante, Becken-Erinnerung, Struktur-Check auf `## Schreibmechanik INBOX-BEFUNDE.md` — Anker unveraendert, traegt |
| `CLAUDE.md:51` | in p3 geaendert; nach F1/F4/F5/F6 in der Triage nachgezogen |
| `DERIVED_STATE_RULES.md:301` | §6.4 „Befoerderung nach INBOX.md" — in p3 um die uebrigen Abgaenge ergaenzt, traegt |
| `lessons.md` L46 | Lektion (Lesestand-Nachfuehrung), keine Verhaltensbeschreibung — traegt |
