# Feature: Ueberwachungs-Tick

**Erstellt:** 2026-09-24
**Ziel:** Der Orchestrator bemerkt Fortschritt, Blockaden und das Ende einer Pane-Session, ohne nachfragen oder blockierend warten zu muessen.
**Prioritaet:** Mittel <!-- per Veto-Vorlage bestaetigt 2026-09-24 -->
**Status:** Abgenommen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Heute sieht der Orchestrator den Stand einer Pane-Session nur, wenn der Mensch danach fragt —
`dtb:pane-start` und der Pane-Traeger von `dtb:worker` schliessen blockierendes Warten bewusst
aus und lassen damit eine Anzeige-Luecke. Ein getakteter, rein lesender Ueberwachungs-Tick
schliesst sie: er prueft in festen Abstaenden Pane-Zustand, Arbeitsfortschritt und Hand-off,
meldet nur Aenderungen und beendet sich selbst. Praxisbeleg: ein Probelauf am 2026-09-23 brachte
in 7 Ticks 3 echte Eingriffe (#102).

---

## Scope / Abgrenzung

### Enthalten
- Eine Pruefliste, die pro Tick nur liest: Zustand der Pane-Session, Arbeitsstand ihres
  Worktrees (neue Commits, ungesicherte Aenderungen, Fortschritt), eingetroffener Hand-off
- Meldung nur bei Aenderung gegenueber dem vorigen Tick
- Selbstende, sobald der Hand-off eingetroffen oder die Pane verschwunden ist
- Beide Pane-Traeger nutzen dieselbe Pruefliste (interaktiver Arbeitsplatz und autonomer Worker)
- Ein Angebot nach der Zustellung mit fertigem Befehl fuer den wiederkehrenden Lauf
  (in Claude Code: `/loop`), Kostenhinweis und Rueckfall fuer Umgebungen ohne wiederkehrenden Lauf <!-- Lint-Override: `/loop` ist der im Zuschnitt 2026-09-24 benannte Harness-Befehl und Gegenstand der Idee #97 -->
- Eine einzige Quelle fuer Pruefliste und Angebot; der zweite Skill verweist und sichert die
  Existenz der Quelle ab

### Nicht enthalten
- Autopilot, Schreibrechte, Autonomie-Governance, Antwortgeber an Frage-Stellen → #98
- Ueberwachung anderer Wartevorgaenge (Build-Pruefung, Repo-Abgleich)
- Ein modellfreier Lauf der Pruefliste (Bezug #45)
- Aenderungen an den Lese-Sichten; ihr Worktree-Block bleibt ohne Ueberwachung

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Dauerlaeufer: der Tick beendet sich nicht (Hand-off verpasst, Selbstende technisch nicht moeglich) | Mittel | Mittel | Zwei unabhaengige Endgruende (Hand-off, Pane weg); Wirklauf belegt das Selbstende; fehlt es, nennt die Endmeldung den Stopp-Weg fuer den Menschen |
| Kosten: jeder Tick belastet den vollen Orchestrator-Kontext | Hoch | Niedrig | Kostenhinweis im Angebot; Tick nur auf Wunsch; Vorschlagstakt 15 Minuten statt kuerzer |
| Meldungs-Rauschen verdraengt echte Signale | Mittel | Mittel | Meldung nur bei Aenderung; Dauerzustaende (blockiert, Zeit ueberschritten) nur einmal |
| Zweite Kommando-Quelle entsteht und driftet | Niedrig | Hoch | Pruefliste lebt nur beim Worker-Traeger; Struktur-Check im anderen Skill; mechanische Pruefung, dass keine neuen Kommandozeilen dort entstehen |
| Status `unknown` wird als Abschluss gelesen | Niedrig | Mittel | Ausdruecklich als Aenderung melden, nie als Ende werten |

---

## Dependencies

### Erforderlich vor Start
- [ ] Keine — Transport, Hand-off-Format und Worktree-Stand-Regel existieren bereits

### Referenz-Dokumente
- `features/ueberwachungs-tick/discovery.md` - betroffene Module, Randfaelle
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` §10 - Worktree-Stand (Signalquelle, per Verweis)
- `dtb-project/project-workflows/INBOX-BEFUNDE.md` #102 - Praxisbeleg des Probelaufs 2026-09-23

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Nach einer Pane-Zustellung liegt dem Menschen ein fertiger, direkt nutzbarer Ueberwachungs-Befehl samt Kostenhinweis und Rueckfall vor — gestartet wird nur auf seinen Wunsch
- [ ] Ein Tick ohne Aenderung erzeugt keine Meldung; ein Tick mit Aenderung meldet sie knapp
- [ ] Der Tick beendet sich nach eingetroffenem Hand-off selbst und nennt den Grund einmal
- [ ] Blockade und Zeitueberschreitung werden gemeldet, ohne dass der Tick etwas beendet oder schreibt
- [ ] Ohne wiederkehrenden Lauf liefert der Zuruf "Stand?" dieselbe Pruefung einmal
- [ ] Pruefliste und Kommandos existieren an genau einer Stelle; der verweisende Skill erkennt deren Fehlen

---

## Offene Punkte

- Laesst sich ein Lauf mit festem Intervall aus sich selbst heraus beenden, oder nur ein selbstgetakteter? Belegt der Wirklauf der Umsetzung

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-09-24)
