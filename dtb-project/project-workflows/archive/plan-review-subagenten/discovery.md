# Discovery: plan-review mit Subagenten
<!-- resume: done -->

**Erstellt:** 2026-11-27
**Idee-Referenz:** Inbox #215 — "`dtb:plan-review` mit echten Subagenten statt Rollenspiel in einem Kontext"
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-plan-review/SKILL.md | Kern: Frontmatter (`allowed-tools` + `Agent`, `consumes` + `workflow.config.yaml`, `description`), Schritt 0 (Modell-Key), Schritt 2 (Rollen als Prompt-Material statt „Rollen einnehmen"), Schritt 3 (Dispatch, Zusammenfuehrung, Fallback), Output-Kopfzeile, „Wichtig" |
| agents/CLAUDE.md | Zweck-Satz („multi-agent skill discussions") und Hinweis: Rollendatei = Subagent-Prompt, bewusst ohne Frontmatter |
| CLAUDE.md | Abschnitt „Agent Roles" — Beschreibung der Nutzung durch plan-review |
| README.md | Zeile `/dtb:plan-review` (Skill-Tabelle) |
| workflow.config.yaml | neuer optionaler Block `plan_review.modelle` |
| skills/dtb-project-init/SKILL.md | Config-Vorlage um denselben Block ergaenzen |

---

## Anforderungen

### Scope
**Enthalten:**
- Jede aktive Rolle (Architekt, Pragmatiker, Senior Dev, Betriebs-Waechter falls aktiviert) laeuft als eigener Subagent; alle Rollen werden in einer Nachricht parallel gestartet
- Eine Rolle sieht die Befunde der anderen nicht — sie bekommt nur Rollentext, Plan-/Spec-Pfad, die Ergebnisse von Grounding (2d) und Challenger-Pass (2e) sowie die gefilterten Lektionen
- Optionales Modell je Rolle ueber `plan_review.modelle` in `workflow.config.yaml` (Default `null` = Modell der Session erben)
- Sichtbarer Fallback, wenn das Agent-Werkzeug fehlt oder ein Subagent scheitert
- Doku-Spiegel (agents/CLAUDE.md, Wurzel-CLAUDE.md, README, project-init-Vorlage)

**Nicht enthalten:**
- Native Agent-Typen (Frontmatter in `agents/*.md`) — per Kernfrage 2026-11-27 verworfen: die Typen erschienen in jeder Session jedes Projekts, und der Projekt-Fallback `agents/` haette keinen nativen Typ
- Zweite Modellfamilie (bleibt #182, autonome Kette)
- Zweite Subagenten-Runde fuer Einspruch-Reaktionen
- Aenderungen an Verdikt-Regel, Finding-Runde (Schritt 5) oder Kopf-Statusfeld (Schritt 6)

### Gewuenschtes Verhalten
- Schritte 0–2e laufen unveraendert im Hauptkontext; danach startet der Haupt-Skill je aktiver Rolle einen general-purpose-Subagenten (Muster wie `dtb:impl-review` Schritt 4–6)
- Jeder Subagent liefert Runden 1–4 aus seiner Perspektive und am Ende seines eigenen Laufs (nach seiner Runde 3) die Verdikte NUR seiner Dimensionen, dazu optional Einsprueche zu fremden Dimensionen
- Der Haupt-Skill ordnet die Rueckgaben ins bestehende Report-Format, rechnet das Gesamt-Verdikt nach der festen Regel, fasst gleiche Befunde in den Empfehlungen zusammen und fuegt den Runden keine eigenen Befunde hinzu
- Die Reaktion auf einen Einspruch schreibt der Haupt-Skill in einem Satz, gekennzeichnet als Haupt-Skill-Reaktion
- Kopfzeile im Report: `🤖 Subagenten: {N}/{M} Rollen isoliert`
- Subagenten sind read-only; geschrieben wird nur im Hauptkontext (Schritt 5/6)

### Randfaelle
- Agent-Werkzeug nicht verfuegbar → alle Rollen im Hauptkontext wie heute, eine ⚠-Zeile; Review bricht nie ab
- Einzelner Subagent scheitert oder liefert eine unbrauchbare Rueckgabe (Verdikt fehlt, fremde Dimension bewertet) → diese Rolle im Hauptkontext nachholen, ⚠-Zeile je Rolle
- `plan_review.modelle` fehlt, ist `null` oder nennt eine unbekannte Rolle/ein unbekanntes Modell → erben; unbekannter Wert mit einer ⚠-Zeile
- Betriebs-Waechter nicht aktiviert → nur drei Subagenten

### Einschraenkungen
- `dtb:plan-review` bleibt worktree-faehig und schreibt weiter nur `features/{slug}/plan.md`
- Laufzeit-Autarkie: alles Noetige inline im Skill (installierte Kopie sieht `skills/CLAUDE.md` nicht)
- Kosten: vier statt eines Modellaufrufs je Review — bewusst in Kauf genommen (Kern der Idee: unabhaengige Urteile)

### Integrationspunkte
- Rollendateien `agents/*.md` (global `~/.claude/agents/`, Fallback Projekt-`agents/`) — Inhalt unveraendert, neue Nutzung als Prompt-Material
- `dtb:feature-fast` Schritt 2 zitiert „Muster wie `dtb:plan-review` Schritt 2" (Aufloesung global → Projekt) — muss gueltig bleiben
- `scripts/lint-skills.py` prueft das geaenderte Frontmatter

---

## Abhaengigkeiten

- Keine aktiven Change-Ordner (features/ leer); Abgrenzung zu #182 (zweite Modellfamilie, autonome Kette)

---

## Offene Punkte

- Soll ein Einspruch spaeter doch an die zustaendige Rolle zurueckgehen (zweite Runde), wenn der Probelauf zeigt, dass die Haupt-Skill-Reaktion das Rollenspiel-Problem wieder einfuehrt? — am Manual-Gate von Phase 1 beurteilen

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-27)
