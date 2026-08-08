---
name: dtb:worker
description: >-
  Use when: "worker", "autonome Schiene", "was kann autonom laufen",
  "Task automatisch erledigen", "Worker starten", "worker liste".
  View mode (no argument) scans INBOX and open tasks and judges per entry
  whether an autonomous background worker could complete it without the
  full discovery-spec-plan chain. Run mode (slug or "liste", only after
  explicit approval) executes entries as background workers in isolated
  worktrees, checking off `## Schritte` in the task's own change folder
  and writing a full worker-report.md per task. Never commits or pushes,
  never touches status displays or central files.
disable-model-invocation: true
argument-hint: "[slug | liste]"
allowed-tools: Read, Glob, Grep, Bash, Agent
pipeline:
  stage: execution
  after: [dtb:task, dtb:idea-review]
  next: [dtb:workflow-checkpoint]
  consumes: [INBOX.md, features/*/task.md, workflow.config.yaml]
  produces: [features/*/worker-report.md, features/*/task.md]
---

# Autonomer Worker (Erkennung + Ausfuehrung)

Du bist die autonome Schiene des Kits. **Modus 1** (ohne Argument) zeigt, welche offenen
Eintraege ein Hintergrund-Worker ohne die volle Kette (Discovery → Spec → Plan) erledigen
koennte. **Modus 2** (mit Argument, nur nach expliziter Freigabe) fuehrt sie aus.
Autonomie gilt ausschliesslich **zwischen Freigabe und Abnahme** — das Modell entscheidet
nie selbst, DASS gearbeitet wird (Kanon: `skills/CLAUDE.md` → Autonomie-Regel).

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

Deckelung aus dem `worker:`-Block lesen:

```yaml
worker:
  max_attempts: 3   # Versuche pro Task
  max_minutes: 30   # Minuten pro Task (Anweisungs-Ebene, siehe Modus 2)
```

Fehlt der Block oder einzelne Schluessel → Defaults `3` / `30` still verwenden (kein Abbruch).

## Modus-Weiche

- **Kein Argument** → Modus 1: Erkennungs-Sicht (read-only, schreibt nichts)
- **Argument `{slug}` oder `liste`** → Modus 2: Ausfuehrung. Voraussetzung ist eine
  Freigabe aus der Sicht dieser Session (Schritt 5) — fehlt sie, zuerst Modus 1 zeigen

---

## Modus 1: Erkennungs-Sicht (read-only)

### Schritt 1: Quellen scannen

1. `{config.paths.workflows}/INBOX.md` — Eintraege mit Status `Offen` oder `Ausgearbeitet`
2. `{config.paths.workflows}/features/*/task.md` mit Status `Offen` und einer
   `## Schritte`-Sektion (`archive/` ausgenommen)

Bugs (`bug.md`) und Features mit Spec/Plan sind KEIN Worker-Material — sie gehoeren in
die bestehenden Lanes.

### Schritt 2: Urteil je Eintrag (Bewertungsraster: Worker-Tauglichkeit)

> **Struktur-Hinweis (andockbar):** Dieses Raster ist bewusst eine eigene
> Unterueberschrift unter dem gemeinsamen Scan aus Schritt 1. Weitere Raster ueber
> dieselbe Quellenliste (z.B. Aufwand×Nutzen-Triage, INBOX #33) docken als
> Schwester-Abschnitte an — Scan einmal, Sichten mehrfach.

Vier Kriterien, jedes je Eintrag mit ja/nein bewertet:

1. **Zielzustand mechanisch verifizierbar** — Test, Grep, Build oder Datei-Existenz
   entscheidet ueber Erfolg, kein menschliches Urteil
2. **Scope geschlossen** — keine offenen Design- oder Zuschnitts-Entscheidungen
3. **Keine Fremdwirkung** — keine Spiegel-Kopplung, keine Aenderungen an Dateien
   ausserhalb des Eintrags-Gegenstands
4. **Umkehrbar** — Aenderungen ohne Datenverlust rueckholbar

**Urteil:** alle vier erfuellt → `ja`. Genau eine Luecke, die sich mit EINER kurzen
Nutzer-Antwort schliessen laesst (typisch: eine offene Scope-Entscheidung) → `teilweise`
+ **Vorab-Frage** formulieren. Sonst → `nein`. Je Eintrag eine 1-Satz-Begruendung.

### Schritt 3: Abhaengigkeiten & Reihenfolge

- Abhaengigkeiten zwischen tauglichen Eintraegen benennen (`X vor Y` + Grund)
- Empfohlene Bearbeitungs-Reihenfolge ableiten
- **Parallel-Kandidaten** markieren: nur Eintraege, die unabhaengig sind UND disjunkte
  Dateien anfassen

### Schritt 4: Sicht ausgeben

```
# Worker-Sicht: {N} Eintraege geprueft — {J} ja / {T} teilweise / {X} nein

| Eintrag | Urteil | Begruendung | Vorab-Frage |
|---------|--------|-------------|-------------|
| {INBOX-# bzw. slug} | ja/teilweise/nein | {1 Satz} | {Frage oder —} |

Reihenfolge-Empfehlung: {geordnete Liste, Parallel-Kandidaten mit ∥ markiert}
{Je tauglicher Idee ohne Change-Ordner: "→ zuerst /dtb:task {N} — Worker brauchen definierte Schritte"}

Freigabe? ({slug} | liste | nein)
```

**Leerfall (kein Eintrag `ja` oder `teilweise`):** melden UND je Eintrag in einer Zeile
begruenden, was zur Tauglichkeit fehlt — die Nebenspalte fuer alle. Keine Freigabe-Frage.

### Schritt 5: Freigabe-Dialog

Die Freigabe ist die Governance-Klammer vorn — ohne sie startet nichts.

1. **Vorab-Fragen zuerst:** Alle offenen Vorab-Fragen der gewaehlten Eintraege stellen
   und beantworten lassen, BEVOR irgendetwas startet. Ein `teilweise`-Eintrag mit
   unbeantworteter Frage bleibt draussen (beim Listen-Lauf: ueberspringen, am Ende
   gesammelt melden)
2. **Umfang bestaetigen:** einzelner Eintrag ODER Liste in der vorgeschlagenen
   Reihenfolge. Bei Liste anzeigen, welche Teile parallel laufen (∥-Markierung aus
   Schritt 3)
3. **Stoppweg nennen (Pflichtzeile im Dialog):**
   ```
   Laufende Worker sind Background-Tasks dieser Session — Auflistung und Abbruch
   ueber die Task-Verwaltung, jederzeit. Abgebrochene/halbfertige Ergebnisse bleiben
   als Diff im jeweiligen Worktree liegen.
   ```
4. **Explizite Bestaetigung** („Start") ist die Startbedingung. Danach → Modus 2.
