# Discovery: idea-rank
<!-- resume: done -->

**Erstellt:** 2026-09-17
**Idee-Referenz:** Inbox #33 — "Aufwand×Nutzen-Triage-Sicht als eigener Skill: sichtet alle offenen INBOX-Ideen und liefert eine priorisierte Ansicht in vier Toepfen (Quick Wins / strategisch wertvoll / wartend-blockiert / braucht eigenen Fokus), je Idee Aufwand- und Nutzen-Einschaetzung, Abhaengigkeiten, empfohlene Reihenfolge — rein lesend. Name entschieden 2026-09-17: `dtb:idea-rank`"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-idea-rank/SKILL.md` | Neubau — der lesende Ranglisten-Skill |
| `skills/dtb-idea-review/SKILL.md` | Frontmatter `pipeline.after` um `dtb:idea-rank` ergaenzen (Gegenkante) |
| `CLAUDE.md` | Kategorie „Idea management" um `idea-rank` ergaenzen |
| `skills/CLAUDE.md` | Tabelle „Skill-Kategorien (Worktree-Verhalten)", Zeile Read-only-Sichten um `idea-rank` ergaenzen |
| `README.md` | Tabelle „Skills Overview" um `/dtb:idea-rank` ergaenzen |

---

## Anforderungen

### Scope
**Enthalten:**
- Alle INBOX-Eintraege mit Status `Offen` lesen und jeden genau einem von vier Toepfen zuordnen:
  **Quick Wins** (kleiner Aufwand, sofort nuetzlich), **strategisch wertvoll** (mittlerer Aufwand,
  lohnt Planung), **wartend/blockiert** (mit benannter Vorbedingung bzw. Blocker-Idee),
  **braucht eigenen Fokus** (nicht nebenbei)
- Je Idee Aufwand (klein/mittel/gross) und Nutzen (niedrig/mittel/hoch) mit 1-Satz-Begruendung
- Abhaengigkeiten zwischen Ideen explizit ausweisen (Muster „#32 zwingend vor #27")
- Empfohlene Bearbeitungs-Reihenfolge als Fazit, abschliessend Hinweis auf `/dtb:idea-review`
- Optionales Argument: Liste von Ideen-Nummern als Teilmenge; ohne Argument alle `Offen`-Ideen
- Registrierung des Skills in `CLAUDE.md`, `skills/CLAUDE.md`, `README.md` und als Gegenkante in `dtb:idea-review`

**Nicht enthalten:**
- Jede Schreibwirkung: keine Statusaenderung in `INBOX.md`, keine Ablage des Ergebnisses als Datei (`produces: []`)
- Das Befund-Becken `INBOX-BEFUNDE.md` — Becken-Eintraege erscheinen in keiner Arbeitssicht (`DERIVED_STATE_RULES.md` §6.4)
- Umbau oder Umbenennung von `dtb:idea-triage` (bleibt Becken-Skill)
- Fortschreiben frueherer Triagen / Delta-Begruendung gegen einen Vorlauf
- Automatische Uebernahme der Reihenfolge durch `dtb:idea-review`

### Gewuenschtes Verhalten
- Report im Chat, gegliedert nach den vier Toepfen; innerhalb jedes Topfs je Idee: Nummer, Kurztitel, Aufwand, Nutzen, 1-Satz-Begruendung
- Blockierte Ideen nennen ihre Vorbedingung konkret (Idee-Nummer, laufendes Feature oder externe Voraussetzung)
- Eigener Abschnitt „Abhaengigkeiten" mit gerichteten Paaren
- Fazit: nummerierte Reihenfolge-Empfehlung, danach Uebergabe-Hinweis `→ /dtb:idea-review`
- Querbelege: `features/*/` (laufende Changes) und `BACKLOG.md` werden lesend herangezogen, um Blocker und Ueberschneidungen zu erkennen; das Changelog wird nicht gescannt
- Jeder Lauf bewertet neu

### Randfaelle
- `INBOX.md` fehlt oder ist leer → Hinweis auf `/dtb:idea`, Ende
- Keine `Offen`-Eintraege → Hinweis „nichts zu ranken", Ende
- Argument nennt eine Nummer, die nicht existiert oder nicht `Offen` ist → je Nummer melden, Rest ranken
- Ideen mit Status `In Arbeit` werden nicht gerankt, aber als Blocker-Kontext genannt, wenn eine offene Idee von ihnen abhaengt
- Eine einzige offene Idee → Report trotzdem vollstaendig (ein Topf belegt, Reihenfolge trivial)
- Ideen-Text mit Teil-Routing-Vermerk (Lektion #19: Status `Offen` mit gerouteten Teilen) → nur den ungerouteten Rest bewerten

### Einschraenkungen
- Rein lesend: `allowed-tools` ohne Schreibwerkzeuge
- Grobe Stufen statt Zahlen/Quoten (Lektion #10: keine Schein-Messbarkeit)
- Laeuft im verlinkten Worktree unveraendert (Kategorie Read-only-Sicht)
- Der Zaehlbegriff „offen" ist der INBOX-Status `Offen` — keine eigene Neudefinition (Lektion #45)

### Integrationspunkte
- Pipeline: `stage: idea`, `after: null`, `next: [dtb:idea-review]`; Gegenkante in `dtb:idea-review` `after`
- `dtb:kit-sync` verteilt den Skill automatisch ueber das Klasse-A-Muster `skills/dtb-*/SKILL.md`
- `dtb:workflow-status`/`dtb:pipeline-graph` lesen die Kanten aus dem Frontmatter

---

## Abhaengigkeiten

- Keine blockierenden. Namenskonflikt mit `dtb:idea-triage` am 2026-09-17 durch eigenen Namen aufgeloest.

---

## Offene Punkte

- Stufenwahl „Topf" bei Grenzfaellen (z.B. kleiner Aufwand, aber niedriger Nutzen): Zuordnungsregel beim Bau in Schritt 1.2 festlegen und im Probelauf pruefen

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-09-17)
