# Review-Snapshot: seed-skew-aktiv-melden
Scope: CLAUDE.md, skills/CLAUDE.md, skills/dtb-kit-sync/SKILL.md (+ 3 Workflow-Artefakte) · Geprueft bis: `3b6d00d` · Datum: 2026-11-09
Gesamt-Verdikt: NEEDS ATTENTION

## Verdikt-Achsen

| Achse | Verdikt |
|-------|---------|
| Plan Adherence | WARNING |
| Scope Discipline | PASS |
| Safety & Quality | WARNING |
| Architecture | WARNING |
| Pattern Consistency | WARNING |
| Rules | uebersprungen |

## Findings
### F1 — Safety & Quality — [S:Mittel × I:Hoch]
skills/dtb-kit-sync/SKILL.md:248-250 — Vergleich laeuft gegen den geklonten Commit, die Abhilfe-Befehle (Vergleichen/Uebernehmen) gegen den Arbeitsbaum von localPath; der pull-Hinweis veraendert den Entwicklungs-Klon und pullt den ausgecheckten Branch statt {REF}.
Fix: Befehle an den verglichenen Commit binden (git -C {localpath} fetch; git -C {localpath} show {COMMIT}:… > {pfad}), pull-Hinweis streichen.
Decision: FIXED

### F2 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-kit-sync/SKILL.md:225 — Bei WERKZEUG-FEHLSCHLAG erscheint „Alles synchron — keine Aktion noetig", obwohl der Seed nicht verglichen wurde.
Fix: eigene Schlusszeile „Kit-Kopien synchron — Seed-Vergleich fehlgeschlagen (siehe oben)".
Decision: FIXED

### F3 — Safety & Quality — [S:Mittel × I:Mittel]
skills/dtb-kit-sync/SKILL.md:183 — Leere Projekt-Regeldatei wird als Werkzeug-Fehlschlag eingestuft und versteckt damit einen kaputten Seed.
Fix: Projektseite nur auf Lesbarkeit pruefen (-r); leere Datei → WEICHT-AB mit 0 Zeilen.
Decision: FIXED

### F4 — Pattern Consistency — [S:Mittel × I:Niedrig]
skills/dtb-kit-sync/SKILL.md:174 — localPath wird nicht als Verzeichnis geprueft (project-init Schritt A tut es); nach Rechnerwechsel Befehle auf toten Pfad.
Fix: [ -d "$LP" ] || LP="" — dann greift die Variante „von Hand vergleichen".
Decision: FIXED

### F5 — Architecture — [S:Niedrig × I:Mittel]
skills/dtb-kit-sync/SKILL.md:184-185 — Gate „Hash nicht leer" greift nie (leere Eingabe ergibt einen Hash); ein Lesefehler wird zu einem scheinbaren WEICHT-AB.
Fix: Einlese-Fehler per pipefail auffangen und als WERKZEUG-FEHLSCHLAG melden.
Decision: FIXED

### F6 — Pattern Consistency — [S:Niedrig × I:Mittel]
skills/dtb-kit-sync/SKILL.md:177 — Regelpfad-Parsing nimmt das erste eingerueckte rules: in beliebigem Block; einfache Anfuehrungszeichen bleiben stehen.
Fix: auf den paths:-Block verankern, beide Quote-Arten und Kommentare entfernen.
Decision: FIXED

### F7 — Pattern Consistency — [S:Niedrig × I:Niedrig]
skills/dtb-project-init/SKILL.md:306-309, skills/dtb-idea-triage/SKILL.md:91-92 — zitieren Wortlaut, den der Change entfernt hat („Seed via project-init", „never drift-checked").
Fix: beide Zitate auf den neuen Wortlaut ziehen, per Grep mit Zielzahl pruefen.
Decision: FIXED

### F8 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-kit-sync/SKILL.md:186-187 — key=value-Ausgabe durch Leerzeichen getrennt; Pfade mit Leerzeichen machen sie mehrdeutig.
Fix: ein Feld pro Zeile ausgeben.
Decision: FIXED

### F9 — Architecture — [S:Niedrig × I:Niedrig]
skills/dtb-kit-sync/SKILL.md:29-31 — „Einzige Lese-Ausnahme" nennt nur die Regel-Datei, gelesen wird auch workflow.config.yaml.
Fix: beide Dateien nennen.
Decision: FIXED

### F10 — Plan Adherence — [S:Niedrig × I:Niedrig]
features/seed-skew-aktiv-melden/spec.md (## Scope / Abgrenzung → Enthalten) — nennt noch dtb:project-init als Abhilfe, entgegen der Entscheidung aus Schritt 1.1.
Fix: Satz auf „Uebernahme von Hand mit fertigen Befehlen" aendern.
Decision: FIXED
