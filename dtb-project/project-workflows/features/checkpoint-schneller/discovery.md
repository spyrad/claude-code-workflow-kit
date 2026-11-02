# Discovery: Checkpoint schneller
<!-- resume: done -->

**Erstellt:** 2026-11-02
**Idee-Referenz:** Inbox #177 — "Kette straffen (1/4, zuerst): `dtb:workflow-checkpoint` schneller machen — erst an 3–5 echten Laeufen messen, welcher Schritt die Minuten kostet, dann Teile, die selten etwas finden, bedingt machen. Fertig, wenn: Median ≤ 4 aktive min (chain-metrics) und der verschlankte Checkpoint findet in 3 Vergleichslaeufen dieselben Lektionen, Fach-Fragen und Entscheidungen wie der bisherige."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-workflow-checkpoint/SKILL.md` | Schritt 0 (Sammelvorlage der Verlustfunde), Schritt 1 (Aufgaben-Vergleich, Zuordnungsfragen, ⏳-Vorlage, Z. 599–624), Schritt 4b (Dashboard, Schalter Z. 712), Schritt 6 (Bestaetigung) |
| `skills/CLAUDE.md` | Abschnitt „Rueckfragen-Defaults (Veto-Form)" → Zuordnungstabelle (letzte Zeile heute H) |
| `CLAUDE.md` | Kurzbeschreibung von `workflow-checkpoint` unter „Session lifecycle" |
| `README.md` | Z. 100: Dashboard „refreshed by `workflow-checkpoint` unless `dashboard.bei_checkpoint: false`" |
| `skills/dtb-project-dashboard/SKILL.md` | Z. 25 und 53: beschreibt den Aufruf aus Checkpoint-Schritt 4b |
| `skills/dtb-project-init/SKILL.md` | Z. 113 und 129: Config-Vorlage und Erklaerung `dashboard.bei_checkpoint` |
| `dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-phasen.py` | Mess-Skript (Neubau, bei der Erhebung im Scratchpad entstanden und hierher gesichert) |
| `dtb-project/project-workflows/features/checkpoint-schneller/checkpoint-rueckfragen.py` | Diagnose der Rueckfragen nach Art (Neubau, ebenso gesichert) |

---

## Messung (Vorher-Werte, 2026-11-02)

Read-only-Auswertung der Claude-Code-Transkripte auf dem Arbeitsrechner (`~/.claude/projects/*/*.jsonl`,
nur Hauptsitzungen, keine Subagenten). 165 Sitzungsdateien, 107 Checkpoint-Segmente im Zeitraum
2026-10-05 bis 2026-11-02: 19 Worktree-Abbrueche (Sende-Seite), 13 ohne Schreibvorgang, 74 normale
Laeufe (davon 2 Hand-off-Empfaenge). Luecken je hoechstens 5 min wie in `chain-metrics.py`.
Die Protokolle reichen nur 30 Tage zurueck — deshalb sind Skript und Zahlen hier versioniert.

| Groesse | Wert |
|---------|------|
| Segment-Median (wie chain-metrics: bis zum naechsten Slash-Befehl) | 6,9 min |
| Kern-Median (bis zum letzten Schreibvorgang des Checkpoints) | 4,8 min |
| Kern-Median bis 2026-10-20 / 10-21..26 / ab 10-27 | 4,2 / 4,8 / 5,3 min |

Anteile an der Kern-Zeit (74 Laeufe):

| Teil | Median min | Anteil |
|------|-----------|--------|
| Warten auf den Menschen | 1,2 | 39 % |
| Verlustpruefung (Schritt 0) | 0,9 | 22 % |
| Sammeln, Aufgaben-Vergleich (Schritt 1) | 0,4 | 14 % |
| Status-Sync (Schritt 2) | 0,2 | 9 % |
| Dashboard (Schritt 4b, nur seit 2026-10-27; dort Median 1,1, max. 7,3) | 0,0 | 7 % |
| Start, Log, Status, Abschluss zusammen | — | 7 % |

Wartezeit nach Art der Rueckfrage (ganzes Segment, 176 Antworten des Menschen):

| Rueckfrage | Anzahl | Anteil der Wartezeit |
|------------|--------|----------------------|
| Commit/Push nach dem Checkpoint | 55 | 35 % |
| sonstiges Gespraech (u. a. Folgearbeit nach dem Checkpoint) | 42 | 25 % |
| Sammelvorlage der Verlustfunde | 38 | 19 % |
| Abnahme/Status-Frage | 19 | 11 % |
| ⏳-Alters-Vorlage | 11 | 5 % |
| Merge/naechster Schritt | 10 | 5 % |
| Weiche Wechsel/Ende | 1 | 1 % |

> Nachtrag 2026-11-02 (Umsetzung, Schritt 2.1): Das fertige `checkpoint-phasen.py --rueckfragen`
> ordnet ueber die letzten 400 statt 170 Zeichen der Modell-Nachricht zu und trifft dadurch mehr
> Vorlagen: Commit/Push 38 % (55), Sammelvorlage 25 % (53), Abnahme 16 % (31), ⏳ 9 % (16),
> sonstiges 9 % (14). no-loss-check inline 10 statt 13, ohne Spur 13 statt ~10 (engeres Muster).
> Laeufe, Mediane und Phasen-Anteile sind identisch; die Aussage aendert sich nicht. Fuer die
> Nachmessung gelten die Werte des fertigen Skripts als Vorher-Werte.

Weitere Befunde:
- Die Commit-Frage steht nicht im Skill-Text (Grep auf `committen|commit-and-push` in
  `skills/dtb-workflow-checkpoint/SKILL.md` trifft nur Z. 276, ein Feld der Uebergabe-Notiz) — das
  Modell stellt sie von sich aus, meist als Freitext „Soll ich committen?"
- Rueckfragen laufen fast nur als Freitext (Mittel 2,4 je Lauf), Auswahlfragen kaum (Mittel 0,1)
- `no-loss-check`: in 51 von 74 Laeufen per Skill-Aufruf, in 13 inline ohne Skill-Aufruf (Ausgabe
  „Verlustpruefung — N Fund(e)"), in rund 10 kurzen Laeufen ohne Spur. Die Luecke „66 Starts bei
  133 Laeufen" in chain-metrics zaehlt also Skill-Aufrufe, nicht Pruefungen
- Die Sammelvorlage der Verlustfunde erschien in 38 von 74 Laeufen — die Verlustpruefung findet oft
  etwas und ist kein Kandidat fuer „selten noetig"

---

## Anforderungen

### Scope
**Enthalten:**
- Die Commit-Frage nach dem Checkpoint durch eine feste Weiter-Zeile ersetzen
- Die Rueckfrage-Runden vor dem Schreiben zu einem Kontrollpunkt buendeln: Verlust-Sammelvorlage,
  Zuordnungsfragen des Aufgaben-Vergleichs und ⏳-Alters-Vorlage in einer Nachricht
- Die Dashboard-Auffrischung bedingt machen: nur wenn die Seite schon existiert
- Mess-Skript und Vorher-Werte im Change-Ordner sichern; Doku und Spiegel nachziehen

**Nicht enthalten:**
- Aenderungen an `dtb:no-loss-check` oder an der Verlustpruefung selbst (sie bleibt immer an)
- Aenderungen an `dtb:project-dashboard` (Erzeugung bleibt, wie sie ist)
- Die Abnahme-Frage samt Beleg-Rueckfrage (bleibt eigene Entscheidung beim Menschen)
- Die Sende-Seite im verlinkten Worktree (Weiche Wechsel/Ende, Hand-off-Block, Uebergabe-Notiz)
- Ein Commit innerhalb des Checkpoints (bleibt bei `dtb:commit-and-push`)
- Die Rueckfragen von `impl-review` (#180) und die uebrigen Teile der Ketten-Straffung (#178, #179)

### Gewuenschtes Verhalten
- Der Checkpoint endet mit `→ Weiter mit: /dtb:commit-and-push` und fragt nicht, ob committet werden soll
- Vor dem Schreiben gibt es hoechstens EINE Rueckfrage-Runde: alle vorlage-faehigen Verlustfunde,
  unsichere Zuordnungen und faellige ⏳-Aufgaben stehen in einer Nachricht; der Mensch antwortet
  einmal (z. B. „Ok, passt" oder „streiche 2, 1 erledigt")
- Hat nur einer der Teile Inhalt, erscheint nur dieser Teil — ohne leere Abschnitte
- Die Dashboard-Seite wird nur aufgefrischt, wenn sie im Projekt schon existiert und der Schalter an ist
- Die Verlustpruefung laeuft unveraendert und findet dieselben Lektionen, Fach-Fragen und Entscheidungen

### Randfaelle
- Keine vorlage-faehigen Verlustfunde und keine faelligen Aufgaben → keine Rueckfrage-Runde
- Nur Verlustfunde oder nur ⏳-Aufgaben → nur der jeweilige Teil
- Mehr als 10 Verlustfunde → die bestehende Rueckfall-Regel (Befehle statt Vorlage) gilt weiter;
  die ⏳-Aufgaben erscheinen trotzdem
- Hand-off-Empfang: die offenen Punkte aus dem Block fliessen in den Aufgaben-Vergleich wie bisher
- Unklare Antwort auf die gebuendelte Vorlage → die bisherigen Rueckfall-Regeln je Teil (eine
  Rueckfrage, dann Abbruch des betroffenen Teils, nie stiller Auto-Write)
- Dashboard-Seite fehlt bei `bei_checkpoint: true` → Schritt still ueberspringen
- Verlinkter Worktree → Voll-Guard bricht wie bisher vor allem ab; nichts davon wirkt dort

### Einschraenkungen
- Die Verlust-Pruefung darf nichts verlieren — „Fertig, wenn" verlangt dieselben Funde wie bisher
- Laufzeit-Autarkie: installierte Skills sehen `skills/CLAUDE.md` nicht; die Regeln stehen inline im Skill
- Kopplungs-Hinweise am Checkpoint (Format von `no-loss-check`, §9-Kopie, Dashboard-Anker) bleiben gueltig
- Ein Probelauf ist im Worktree nicht moeglich (Voll-Guard) — er laeuft im Haupt-Checkout gegen die
  Worktree-Fassung des Skills
- Die Zielerreichung (Median ≤ 4 min) laesst sich erst nach dem Merge an echten Laeufen messen

### Integrationspunkte
- `dtb:no-loss-check` (Ausgabe-Muster, das die Sammelvorlage liest — unveraendert)
- `dtb:commit-and-push` (Ziel der Weiter-Zeile)
- `dtb:project-dashboard` (Aufruf aus Schritt 4b, Modus „ohne Browser")
- `DERIVED_STATE_RULES.md` §9 (Aufgaben-Vergleich und ⏳ — Kopie im Checkpoint)
- `chain-metrics.py` im Nachbar-Repo mega.dev (Zielgroesse „aktive min")

---

## Abhaengigkeiten

- Keine blockierenden. Benachbart: #178–#181 (weitere Ketten-Straffung) und #182 (autonome Kette) —
  sie beruehren andere Skills; #182 profitiert von weniger Rueckfragen im Checkpoint

---

## Offene Punkte

- Nachmessung nach dem Merge: Median der aktiven Minuten nach mindestens 10 Laeufen (chain-metrics und
  `checkpoint-phasen.py`), spaetestens 2026-12-02 wegen des 30-Tage-Fensters der Protokolle
- 3 Vergleichslaeufe nach dem Merge: dieselben Lektionen, Fach-Fragen und Entscheidungen wie zuvor
- Reicht die Ersparnis nicht fuer ≤ 4 min, ist der naechste Hebel `dashboard.bei_checkpoint` mit
  Default `false` (spart rund 1 min je Lauf in jedem Projekt mit Seite)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-02)
