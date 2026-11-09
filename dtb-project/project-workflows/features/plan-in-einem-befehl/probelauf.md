# Probelauf: Plan in einem Befehl

**Erstellt:** 2026-11-09 (Phase 2 von `plan.md`)

---

## Verweis-Sweep

Grep `feature-plan` über `skills/`, `agents/`, `output-styles/`, `CLAUDE.md`, `README.md` (ohne
`skills/dtb-feature-plan/` selbst), 2026-11-09. Entscheidung je Treffer:

| Fundstelle | Inhalt | Entscheidung |
|------------|--------|--------------|
| `CLAUDE.md` Lebenszyklus „Work" | feature-plan als Planungs-Befehl | **geändert** — ein Befehl bis `plan.md`, `nur-spec` |
| `CLAUDE.md` Kategorie „Feature workflow" | feature-plan, impl-plan als getrennte Einträge | **geändert** — Referenz-Ausführung, Stopp, impl-plan weiter einzeln aufrufbar |
| `README.md` Skill-Tabelle | „Create structured feature specifications" | **geändert** — plus `plan.md` im selben Lauf |
| `skills/dtb-feature-discover/SKILL.md` Schritt 8 | `Naechster Schritt: /dtb:feature-plan` | **geändert** — Zusatz „(erzeugt spec.md und plan.md)" |
| `skills/dtb-feature-discover/SKILL.md` Frontmatter `next` | `[dtb:feature-plan, dtb:feature-fast]` | bleibt richtig |
| `skills/CLAUDE.md` Hard-Gate-Tabelle (impl-plan → Redirect feature-plan) | Erzeuger von `spec.md` | bleibt richtig — feature-plan erzeugt weiter die Spec |
| `skills/CLAUDE.md` Capture-Gegenprobe (Interview-Synthesen) | feature-plan speichert Synthesen | bleibt richtig |
| `skills/CLAUDE.md` Rückfragen-Defaults Z3 (`feature-plan` Schritt 10) | Backlog als stille Anzeige | bleibt richtig — Punkt 10 behält Nummer (Einschub `8a`), feste Zeile jetzt mit `{Status}` |
| `skills/CLAUDE.md` Worktree-Kategorien (Teil-Guard) | feature-plan Teil-Guard | bleibt richtig — `plan.md` liegt im eigenen Change-Ordner |
| `skills/dtb-feature-fast/SKILL.md` (Struktur-Check, Lint, „analog feature-plan Schritt 10") | Template-Anker, Lint, Backlog-Analogie | bleibt richtig — Anker und Nummer unverändert |
| `skills/dtb-impl-plan/SKILL.md` (`after`, Gate-Redirect, Verwandte, 5 Wartungs-Hinweise) | Vorgänger/Erzeuger der Spec | bleibt richtig; Hinweise in Phase 1 ergänzt |
| `skills/dtb-greenfield-prd/SKILL.md` Lint-Kopie | Leak-Lint-Kopplung | bleibt richtig — Lint unverändert |
| `skills/dtb-open-question`, `skills/dtb-meeting-dump` | feature-plan schreibt `spec.md` | bleibt richtig |
| `skills/dtb-backlog-status`, `dtb-project-init`, `dtb-workflow-status` (Tabellen), `dtb-workflow-next` (Leer-Zustand, „discovery ohne spec") , `dtb-pane-start` | Einstieg „Feature planen" / Spec ausstehend | bleibt richtig — der Befehl ist derselbe, er liefert nur mehr |
| `skills/dtb-archive`, `dtb-idea-rank`, `dtb-project-health`, `dtb-workflow-next`, `dtb-workflow-status` („Change fehlt"-Zweig) | discovery vorhanden → `/dtb:feature-plan` | bleibt richtig |
| `skills/dtb-pipeline-graph/SKILL.md` Beispielkette | `feature-plan → impl-plan → plan-review` | bleibt richtig — beide Skills bestehen weiter; der Graph liest `next:` aus dem Frontmatter (`[dtb:plan-review, dtb:impl-plan]`) |

Sichten, die bei „spec.md ohne plan.md" `/dtb:impl-plan` empfehlen (`workflow-next`, `workflow-status`,
`pane-start`, `project-health`, `workflow-checkpoint`, `workflow-resume`): bleiben richtig — der Fall
entsteht weiter durch `nur-spec` oder einen ausgefallenen Plan-Teil.

---

## Probelauf

Gefahren 2026-11-09 im verlinkten Worktree `pane-plan-in-einem-befehl`, gegen die **Repo-Fassung**
`skills/dtb-feature-plan/SKILL.md` (Stand `32437ce`, Lektion 74). Schein-Feature „Kit-Version im
README anzeigen". Punkt 8a löst `dtb:impl-plan` auf die installierte Kopie
`~/.claude/skills/dtb-impl-plan/SKILL.md` auf (noch ohne die neuen Wartungs-Hinweise — die Anker
sind identisch).

**Lauf A — Durchlauf** (`/dtb:feature-plan zz-test Plan Durchlauf`, Mini-`discovery.md` vorab angelegt):

| Punkt | Ergebnis |
|-------|----------|
| 1 Discovery | `discovery.md` übernommen |
| 2 Inbox | Die bestehende Ideen-Auswahl würde erscheinen (offene Ideen vorhanden) — **keine neue Frage**, sie gab es auch im Einzel-Lauf von feature-plan; in der Probe als „neues Feature (Discovery vorhanden)" beantwortet |
| 8 Spec | `spec.md` gespeichert (Template feature-plan, Fusszeile `/dtb:feature-plan`) |
| 8a (b) | `🧩 Struktur-Check impl-plan: 5/5 Anker gefunden` (Grep auf die installierte Kopie: Zeilen 28, 61, 92, 198, 258) |
| 8a (c) | `📚 100 Lektion(en) beruecksichtigt` (impl-plan-Filter `impl-plan`/`alle`) · `📂 Ist-Analyse aus discovery.md uebernommen (1 Module, Pfade verifiziert)` · kein vorhandenes `plan.md` → keine Überschreib-Frage · `plan.md` nach Template: `## Ist-Analyse`, `#### Automated`, `## Progress` (1 Zeile), `**Status:** Entwurf` in Zeile 6, Fusszeile `/dtb:impl-plan` · kein Lektion-Kandidat |
| 9/10 | `↷ INBOX.md-/BACKLOG.md-Update uebersprungen (Worktree) — in den Hand-off aufnehmen` |
| 11 | Variante **Durchlauf**: spec- und plan-Pfad, `Naechster Schritt: /dtb:plan-review zz-test Plan Durchlauf` |

Nähte: genau **eine** `📚`-Zeile (feature-plan selbst liest keine Lektionen — die Zeile stammt aus
dem impl-plan-Teil), genau **eine** Abschlussmeldung (die impl-plan-Bestätigung entfällt). Keine
Rückfrage, die es in getrennten Läufen nicht gab.

**Lauf B — nur Spec** (`/dtb:feature-plan zz-test Plan nur Spec nur-spec`, ohne Discovery):

| Punkt | Ergebnis |
|-------|----------|
| 8 Spec | `spec.md` gespeichert |
| 8a (a) | Stopp-Weiche greift → Punkt 8a übersprungen, kein Struktur-Check, keine `📚`-Zeile |
| 9/10 | `↷`-Zeile wie Lauf A |
| 11 | Variante **nur Spec**: `Naechster Schritt: /dtb:impl-plan zz-test Plan nur Spec` |

Ergebnis Ordner: `zz-test-plan-durchlauf/` = `discovery.md plan.md spec.md`; `zz-test-plan-nur-spec/` = `spec.md`.

**Nicht ausführbar hier:** Backlog-Zweig im Worktree nicht ausführbar (Teil-Guard + Testordner) — bei
der Abnahme im Haupt-Checkout sichtbar. Belegt ist er nur textlich (Phase-1-Kriterium „Backlog-Zweig
kennt beide Ausgänge"). Ebenfalls nicht gefahren: die beiden Fehlerpfade des Struktur-Checks
(Datei fehlt / Anker fehlt) — sie hätten eine Manipulation der installierten Kopie verlangt.

**Grenze der Probe:** Das Modell, das den Skill geschrieben hat, hat ihn auch ausgeführt — die Probe
belegt, dass der Text vollständig und widerspruchsfrei befolgbar ist, nicht, wie eine frische
Session ihn liest. Den Erstbeleg mit frischem Blick liefert der erste echte Lauf nach dem Merge.

Wegwerf-Ordner nach der Probe gelöscht.

---

## Konsistenz

Anker-Greps gegen die Repo-Fassungen, 2026-11-09 (zeilenverankert, ERE):

| Leser | Quelle | Anker | Fundzahl |
|-------|--------|-------|----------|
| `dtb:feature-fast` | `skills/dtb-feature-discover/SKILL.md` | `^## Schritt 6` | 1 |
| `dtb:feature-fast` | `skills/dtb-feature-plan/SKILL.md` | `^## Template fuer spec.md` | 1 |
| `dtb:feature-fast` | `skills/dtb-feature-plan/SKILL.md` | `^## Technical-Leak-Lint` | 1 |
| `dtb:feature-fast` | `skills/dtb-impl-plan/SKILL.md` | `^## Template fuer plan\.md` | 1 |
| `dtb:feature-plan` 8a | `skills/dtb-impl-plan/SKILL.md` | `^## Lektionen als Prior lesen` | 1 |
| `dtb:feature-plan` 8a | `skills/dtb-impl-plan/SKILL.md` | `^## Codebase-Research \(Ist-Analyse\)` | 1 |
| `dtb:feature-plan` 8a | `skills/dtb-impl-plan/SKILL.md` | `^## Template fuer plan\.md` | 1 |
| `dtb:feature-plan` 8a | `skills/dtb-impl-plan/SKILL.md` | `^## Wichtig - Anweisungen fuer die Ausfuehrung` | 1 |
| `dtb:feature-plan` 8a | `skills/dtb-impl-plan/SKILL.md` | `^## Lektion-Kandidat erkennen \(Vorschlager\)` | 1 |

Zusätzlich: die installierte Kopie `~/.claude/skills/dtb-impl-plan/SKILL.md` trägt alle 5 Anker
(5 Treffer) — feature-plan 8a läuft also auch vor dem nächsten `kit-sync` grün. Feste Zeile der
Rückfragen-Defaults `→ in BACKLOG.md eingetragen (Status: {Status})` steht jetzt wörtlich in
feature-plan (1 Treffer; vorher mit festem Wert `Spezifiziert`).

Alle Fundzahlen = 1.
