# Aufgabe: INBOX-Migration in das Befund-Becken

**Erstellt:** 2026-09-09
**Prioritaet:** Mittel
**Status:** In Arbeit
**Bereich:** Projekt-Artefakte — `dtb-project/project-workflows/INBOX.md`, `INBOX-BEFUNDE.md`

---

## Beschreibung

Der Umbau aus Feature `ideen-becken` (INBOX #76) ist abgenommen, aber das Becken startet
bewusst leer: `features/ideen-becken/spec.md:48` klammert die Migration des Altbestands als
eigenen Lauf danach aus, damit die Abnahme nicht an Urteilsfragen haengt. Damit stehen die
maschinellen Verlustfunde weiter in `INBOX.md` — genau der Zustand, den #76 aufloesen wollte.

Diese Aufgabe fuehrt den Migrationslauf aus. Die Ursprungs-Zuordnung liegt bereits vollstaendig
vor (erhoben 2026-09-09, unten) und muss nicht neu ermittelt werden.

## Begruendung

Die Zuordnung ist **nicht aus den Artefakten ableitbar**: `INBOX.md` traegt kein Herkunftsfeld,
und formal hat der Mensch jeden Eintrag abgesetzt (`dtb:idea` ist `disable-model-invocation`).
Sie wurde am 2026-09-09 aus drei Spuren rekonstruiert — Einfuege-Commit je Zeile
(`git log -S`), Erfassungs-Kontext im Session-Log, und Textmuster (Belegdatum,
Datei:Zeile-Zitat, Lauf-Herkunft). Ohne diese Liste kostet der Migrationslauf die Erhebung
erneut, mit dem Risiko einer abweichenden Einordnung.

Die Erhebung korrigiert dabei die Schaetzung in #76: dort „24 von 37 tragen ein Beleg-Muster",
tatsaechlich sind es **31 von 38** maschinelle Funde. Der Unterschied ist ein
Kriterienunterschied, kein Widerspruch — #76 zaehlte das formale Beleg-Muster, die Erhebung
ordnet zusaetzlich belegfreie, aber unverkennbar analytische Eintraege zu.

## Ursprungs-Zuordnung (Stand 2026-09-09, 38 Eintraege)

### Bleiben in `INBOX.md` — Fach-Wuensche des Menschen (7)

| # | Idee | Merkmal |
| --- | ---- | ------- |
| 57 | Immer gleich beantwortete Rueckfragen automatisieren | „Beobachtung aus der laufenden Praxis", „**Genannte** Beispiele" |
| 45 | Wo passen Claude-Code-Hooks ins Kit? | Pruefauftrag, offene Frage, kein Beleg |
| 41 | Claude Code zum Sprechen bringen (TTS) | externer Wunsch, kein Kit-Bezug |
| 39 | Stitch von Google integrieren? | externer Link, Frageform |
| 33 | Aufwand-Nutzen-Triage-Sicht als Skill | Feature-Wunsch mit Namensvorschlag, kein Belegfall |
| 27 | `grill-me`-Skill von Matt Pocock evaluieren | externer Link, Frageform |
| 15 | `10x-health-check`-Pendant bauen | Vorbild Kurs-Repo, Commit `ecf21b4` „INBOX: 4 neue Ideen erfasst" |

Gemeinsamer Nenner: kein Belegdatum, kein Datei:Zeile-Zitat, Frage- oder Wunschform — drei
zeigen nach aussen (Stitch, grill-me, 10x-Kurs), wohin das Modell im Session-Kontext nicht schaut.

### Nach `INBOX-BEFUNDE.md` — maschinelle Funde (31)

#76, #75, #74, #73, #71, #70, #69, #66, #64, #63, #62, #61, #60, #59, #58, #56, #55, #54,
#53, #52, #51, #47, #46, #44, #35, #34, #32, #31, #23, #22, #18

Signaturen (meist kombiniert): Belegzeile mit Datum („Belegt 2026-08-07", „Gemessen
2026-08-20") · Datei:Zeile-Zitate (`dtb-worker/SKILL.md:196-197`, `.gitignore:10-13`,
„Z. 97/103/109") · Herkunft aus einem Lauf (impl-review-Triage, `worker-report.md`,
no-loss-check/Checkpoint). Commit-Beleg: #52/#53/#54 stammen alle aus
`b5e11e4 fix(feature-start-statusfeld): impl-review Triage - 9 Findings behoben`,
#57 aus `eeac392` — Review-Nebenfunde, keine Einfaelle.

### Veto-Kandidaten (6)

#18, #22, #23, #34, #60, #71 — hier entscheidet Ton und Entstehungskontext, nicht ein
Beleg-Muster. #18 und #60 waren in der Erhebung zunaechst Grenzfaelle und wurden am
2026-09-09 ausdruecklich als maschinell bestaetigt. Bei diesen sechs ist das Veto je Nummer
(Design-Vorgabe aus #76) tatsaechlich wirksam, bei den uebrigen 25 ist es Formsache.

## Schritte

- [x] Zuordnung gegen den aktuellen INBOX-Bestand abgleichen — seit 2026-09-09 koennen
      Eintraege hinzugekommen oder geschlossen sein; neue Eintraege ab #77 sind bereits
      strukturell getrennt und nicht Teil der Migration
- [x] Vetobare Sammelvorlage bauen (Muster `feature-fast`, Vorgabe `discovery.md:52`):
      alle 31 Nummern mit Kurztitel, Veto je Nummer moeglich, die 6 Veto-Kandidaten
      hervorgehoben. EINE Bestaetigung, danach schreiben
- [x] Verworfene Statuszeilen pruefen: #74 und #73 stehen auf `Verworfen`, #76 und #71 auf
      `Ausgearbeitet` — entscheiden, ob entschiedene Eintraege ueberhaupt migrieren oder in
      `INBOX.md` bleiben (ein Becken-Eintrag wird nie gearbeitet, `DERIVED_STATE_RULES.md` §6.4)
- [x] Zeilen nach `INBOX-BEFUNDE.md` uebertragen, Sichtung-Spalte auf `Altbestand`
      (Format `| # | Datum | Befund | Sichtung |`), Nummer unveraendert erhalten
- [x] Feld-Hygiene beim Uebertragen: literale Pipes escapen — #70 und #54 tragen heute bare
      Pipes und brechen ihre Tabellenzeile; die Reparatur gehoert in denselben Lauf (#70 nennt
      sie ausdruecklich als zulaessig, append-only gilt nur fuer `lessons.md`)
- [x] Migrierte Zeilen aus `INBOX.md` entfernen, Tabellenintegritaet beider Dateien pruefen
      (Spaltenzahl je Zeile, keine Nummer doppelt ueber beide Dateien)
- [ ] `WORKFLOW_STATUS.md` und Session-Log ueber `/dtb:workflow-checkpoint` nachziehen
- [ ] Ersten `/dtb:idea-triage`-Lauf ansetzen: 31 `Altbestand`-Eintraege bei Default
      `altbestand_pro_lauf` bedeuten mehrere Laeufe — die Erwartung im Log festhalten

## Durchfuehrung 2026-09-09

Ausgefuehrt: 27 Eintraege nach `INBOX-BEFUNDE.md` (Sichtung `Altbestand`), 11 bleiben in
`INBOX.md`. Abweichung von der Vorab-Zuordnung (31/7) nach Entscheidung des Menschen: die vier
**bereits entschiedenen** maschinellen Eintraege bleiben in der Haupt-INBOX, weil das Becken der
Eingang fuer ungesichtete Funde ist und ein Eintrag dort nie gearbeitet wird —
#76 (`Ausgearbeitet`, `ideen-becken` abgenommen, `/dtb:archive` faellig; `dtb:archive` liest nur
`INBOX.md`), #71 (`Ausgearbeitet`, als Aufgabe geroutet), #74 und #73 (`Verworfen`, umgesetzt).

Verbleibend in `INBOX.md` (11): #76, #74, #73, #71 (entschieden) + #57, #45, #41, #39, #33,
#27, #15 (Fach-Wuensche).

Migriert (27): #75, #70, #69, #66, #64, #63, #62, #61, #60, #59, #58, #56, #55, #54, #53, #52,
#51, #47, #46, #44, #35, #34, #32, #31, #23, #22, #18.

Feld-Hygiene: #70 (5 Felder) und #54 (8 Felder) trugen bare Pipes und brachen ihre Zeile — beim
Uebertragen escapt, beide rendern jetzt mit 4 Feldern.

Verifikation: `INBOX.md` 11 Eintraege, `INBOX-BEFUNDE.md` 34 (7 bestehende + 27 Altbestand),
Nummern-Schnittmenge null, jede Datenzeile beider Dateien genau 4 Felder, Sichtung-Werte nur
`leer` und `Altbestand`. Sicherung der Vorzustaende im Session-Scratchpad.

## Ergebnis

`INBOX.md` traegt nur noch die 7 Fach-Wuensche und spaeter Befoerderte; die 31 maschinellen
Funde stehen in `INBOX-BEFUNDE.md` mit Sichtung `Altbestand` und derselben Nummer wie zuvor.
Keine Nummer existiert doppelt, beide Tabellen rendern intakt (auch #70 und #54). Nachweisbar
an: Zeilenzahl beider Dateien, einem Spaltenzahl-Check je Zeile, und einer Nummern-Schnittmenge
von null zwischen den Dateien.

---

**Erfasst mit:** manuell (Zuordnung erhoben 2026-09-09)
