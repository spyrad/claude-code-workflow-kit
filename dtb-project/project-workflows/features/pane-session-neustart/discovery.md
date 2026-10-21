# Discovery: Pane-Session-Neustart
<!-- resume: done -->

**Erstellt:** 2026-10-21
**Idee-Referenz:** Inbox #142 — "Wenn eine Aufgabe mit /start-new-pane (`dtb:pane-start`) in einem separaten Worktree und separaten Pane gestartet wird und dort das Context-Fenster zu gross wird, ist es umständlich, im bestehenden Pane und Worktree eine neue, frische Session verlustfrei zu starten."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-pane-start/SKILL.md | Begruessungstext + Startbefehl-Tabelle (1b), Fortsetzungsfall; Ort bzw. Nachbar eines Neustart-Wegs |
| skills/dtb-worker/SKILL.md | `### Pane-Ausfuehrung` = einziger Ort fuer Herdr-Kommandos; `/exit` per `agent prompt` kommt als Chat-Text an (belegt 2026-08-16); Ueberwachungs-Tick (gleiche Pane-ID, neue Session) |
| skills/dtb-workflow-checkpoint/SKILL.md | Worktree-Guard + Sende-Seite des WORKTREE-HANDOFF-Blocks; Abgrenzung Zwischenstand vs. Session-Ende |
| skills/dtb-workflow-resume/SKILL.md | Wiedereinstieg einer frischen Session aus Artefakten — Kandidat fuer das Auffinden der Uebergabe |
| skills/dtb-implement/SKILL.md | Schwelle „Kontext verdichtet → Wiedereinstiegs-Kommando" (Ritual Punkt 11) — heute der natuerliche Neustart-Ausloeser |
| skills/CLAUDE.md | „Parallele Sessions" / Skill-Kategorien, Abgrenzung pane-start in der Autonomie-Regel |
| CLAUDE.md | Beschreibung pane-start/worker in der Skill-Liste |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | §10 Worktree-Sicht (frisch/verwaist) — vermutlich nur lesend beruehrt |
| dtb-project/project-rules/lessons.md | Prior (nur lesend): L67 `/clear` behaelt Prozess, L86 rohe Tasten per `pane send-text`, L87 Pane-Status nicht per Regex |

---

## Anforderungen

### Scope
**Enthalten:**
- Definierter Uebergabe-Weg Session → Session innerhalb derselben `dtb:pane-start`-Worktree-Pane, der vier Verlust-Klassen traegt (Praxisfall PKP `simulationsmaske-organisationseinheit`, 2026-10-21):
  1. Pane-Startkontext — Rolle (interaktiv, kein Worker), Orchestrator-Adresse, Schreibgrenzen, Rueckweg-Pflicht (Block woertlich inkl. Kopfzeile)
  2. Aufgelaufene `↷`-Zeilen der Teil-Guards + Hand-off-Punkte aus der Umsetzung, die nicht in `plan.md` stehen
  3. Session-Verlauf — Entscheide, Plan-Abweichungen, Lektions-Kandidaten ausserhalb von `## Lektion-Kandidaten`
  4. Hinweis auf Uncommittetes, das die neue Session mitnehmen muss (z. B. SHA-Rueckschreibung in `plan.md`)
- Die neue Session findet die Uebergabe beim Start selbst — kein Kopieren durch den Menschen
- **Ausloeser ist der Mensch** (Entscheid 1a): er tippt selbst `/clear` bzw. `/exit` + `claude`; das Feature liefert nur „sichern" und „wiederfinden", keine Neustart-Fernsteuerung
- **Ein kumulierter Hand-off am Ende** (Entscheid 2b): Uebergaben akkumulieren ueber alle Sessions der Pane; der Orchestrator erhaelt genau EINEN WORKTREE-HANDOFF-Block, wenn die Arbeit in der Pane endet
- **Uebergabe-Notiz bleibt im Worktree** (Entscheid 3): nicht committet, verschwindet mit dem Abbau des Arbeitsplatzes; ihr Inhalt erreicht das Projekt nur ueber den Hand-off-Block

**Nicht enthalten:**
- Der autonome Pane-Traeger von `dtb:worker` (eigene Governance) — nur `dtb:pane-start`-Arbeitsplaetze
- Sessions im Haupt-Checkout (dort traegt `WORKFLOW_STATUS.md` → `## Handoff`)
- Persistierte Pane-Registry (pane-start schliesst sie bewusst aus)
- Neustart per Herdr-Fernsteuerung (`send-text`/`send-keys`) durch Pane-Session oder Orchestrator
- Zwischen-Bloecke an den Orchestrator je Session-Wechsel

### Gewuenschtes Verhalten
- **Sichern ueber den bestehenden Checkpoint** (Entscheid 3b.1): `/dtb:workflow-checkpoint` fragt in der Pane (verlinkter Worktree) „Session-Wechsel oder Ende der Arbeit?" — Wechsel → schreibt/ergaenzt die Uebergabe-Notiz im Worktree, kein Block an den Orchestrator; Ende → ein kumulierter WORKTREE-HANDOFF-Block (alle Notiz-Staende + aktuelle Session). Kein neuer Skill
- **Wiederfinden ueber den bestehenden Resume** (Entscheid 3b.2): nach `/clear` (bzw. `/exit` + `claude`) tippt der Mensch `/dtb:workflow-resume`; der findet die Notiz im Worktree und stellt Pane-Startkontext, offene Hand-off-Punkte und naechsten Befehl her
- Uebernommenes UX-Muster: Session-Wechsel im Haupt-Checkout (Checkpoint schreibt `WORKFLOW_STATUS.md` → `## Handoff`, Empfehlung „`/clear`, dann `/dtb:workflow-resume`", Resume liest ihn als Empfangsseite) — gespiegelt auf den Worktree mit lokaler Notiz statt zentraler Datei
- Verworfen: eigener neuer Befehl (ein Skill mehr zum Merken); Lesen der Notiz in jedem Arbeits-Skill; SessionStart-Hook (braucht Einstellung je Projekt)

### Randfaelle
1. **Mehrere Wechsel:** Die Notiz waechst append-only um einen Abschnitt je Session — nie ueberschreiben (sonst gehen aeltere Hand-off-Punkte verloren)
2. **Veraltete Orchestrator-Adresse:** `workflow-resume` prueft die Adresse aus der Notiz per Herdr (z. B. `herdr agent get`); ist sie weg → Warnung + Rueckfrage nach der neuen Adresse (ungeprueft uebernommen ginge der End-Block ins Leere)
3. **Direkt `/dtb:implement` statt Resume nach `/clear`:** kein eigener Schutz — der Ende-Checkpoint liest die Notiz ohnehin, nichts geht verloren; es fehlt nur der Startkontext in dieser Session
4. **Worktree ohne Notiz** (Worker-Worktree, manuell angelegt): `workflow-resume` verhaelt sich wie heute, keine Zusatzzeile
5. **Pane endet ohne Checkpoint** (Absturz, geschlossen): Notiz bleibt im Worktree; der naechste Ende-Checkpoint nimmt sie mit. Vor dem Abbau des Arbeitsplatzes warnt ein Hinweis, falls eine noch nicht verschickte Notiz existiert

### Einschraenkungen
- **Ablageort der Notiz = Git-Verwaltungsordner des Worktrees** (`$(git rev-parse --git-dir)/…`, Entscheid 3d.1): wird nie committet, braucht keine `.gitignore`-Zeile (Seeds erreichen Bestandsprojekte nicht, INBOX #22), verschwindet mit `git worktree remove`. Folge: der Abbau loescht sie still — die Warnung aus Randfall 5 ist deshalb Pflicht, nicht Komfort
- **Herdr-Befehl im Resume als benannte Ausnahme** (Entscheid 3d.2): die Adress-Pruefung (Randfall 2) darf in `workflow-resume` stehen — deklarierter Spiegel wie die Rueckweg-Zeile von `pane-start`; der Kanon „Herdr-Kommandos nur in `dtb:worker`" bekommt diese zweite benannte Ausnahme (Kopplungs-Hinweis in beiden Richtungen)
- **Laufzeit-Autarkie:** installierte `workflow-checkpoint`/`workflow-resume` laufen ohne `skills/CLAUDE.md` — Notiz-Format, Pfad und Fragen inline tragen
- **Herdr optional:** ausserhalb von Herdr (kein `HERDR_ENV`) entfaellt nur die Adress-Pruefung; Sichern und Wiederfinden funktionieren ohne Herdr
- Fachliche Constraints: keine

### Integrationspunkte
- `dtb:workflow-checkpoint` — Worktree-Guard bekommt die Weiche „Wechsel oder Ende?"; Wechsel schreibt/ergaenzt die Notiz, Ende baut den kumulierten Block (Format unveraendert aus `### Hand-off-Block`); Empfangsseite im Orchestrator unveraendert
- `dtb:workflow-resume` — findet die Notiz im Worktree, stellt Startkontext her, prueft die Orchestrator-Adresse (Herdr-Ausnahme, 3d.2)
- **Warnung vor dem Abbau nur an EINER Stelle** (Entscheid 3e.1): Abbau-Anleitung `dtb:worker` → `#### Abschluss (nach menschlicher Diff-Abnahme)` (von `pane-start` per Referenz genutzt) — vor `git worktree remove` pruefen, ob eine ungesendete Notiz existiert. Bewusst NICHT in den Worktree-Zeilen von `workflow-next`/`workflow-resume`/`backlog-status` bzw. DSR §10 (vier Spiegel)
- **Wechsel-Weg an zwei Stellen angekuendigt** (Entscheid 3e.2):
  - Begruessungstext von `dtb:pane-start` — sonst kennt die erste Session den Weg nicht
  - Schwellen-Zeile von `dtb:implement` (Ritual Punkt 11, „Schwelle erreicht … weiter in neuer Session") — im Worktree als „erst `/dtb:workflow-checkpoint` (Wechsel), dann `/clear`, dann `/dtb:workflow-resume`"
- Externe Abhaengigkeiten: Git (Pflicht), Herdr (optional — nur Adress-Pruefung)
- Kopplungen mitziehen: Struktur-Check von `pane-start` (Anker in `dtb:worker`), Herdr-Ausnahmen-Liste in `dtb:worker` → `### Pane-Auftrag`, Skill-Kategorien in `skills/CLAUDE.md` (Checkpoint bleibt Voll-Guard, bekommt aber einen Worktree-Schreibweg in den Git-Verwaltungsordner — Kategorie-Text praezisieren)

---

## Abhaengigkeiten

- Keine aktiven Change-Ordner — keine Konflikte
- Beruehrung INBOX #98 (Auto-Mode/Autopilot: Orchestrator steuert Panes selbst) — startet er kuenftig Sessions neu, nutzt er denselben Wechsel-Weg; heute kein Konflikt
- Beruehrung INBOX #110 (Datenschutz-Schalter fuer artefakt-schreibende Skills) — die Notiz traegt Session-Inhalte, bleibt aber lokal im Git-Verwaltungsordner; Merkpunkt fuer #110

---

## Offene Punkte

- Notiz-Format festlegen: Dateiname im Git-Verwaltungsordner, Kopf (Pane-Startkontext einmalig) + append-only Abschnitt je Session; Felder moeglichst 1:1 auf den Hand-off-Block abbilden, damit der Ende-Checkpoint mechanisch kumulieren kann
- „Ungesendet" erkennbar machen (Randfall 5): Markiert der Ende-Checkpoint die Notiz als gesendet, oder loescht er sie? Herdr bestaetigt die Zustellung nicht — Entscheidung in der Spec
- Weiche „Wechsel oder Ende?" nur in `pane-start`-Arbeitsplaetzen (Pfad `.dtb-worktrees/pane-{slug}`) oder in jedem verlinkten Worktree? Worker-Pane-Traeger ist ausgeschlossen (Scope), manuelle Worktrees offen
- Form der Weiche nach Rueckfragen-Defaults (`skills/CLAUDE.md`): Knopf oder Textzeile, Default-Option
- Woher die erste Session den Pane-Startkontext fuer die Notiz nimmt: aus dem Begruessungstext im eigenen Verlauf; nach einer Verdichtung (Kompression) kann er fehlen — Rueckfall definieren (z. B. Orchestrator-Adresse erfragen)
- Fluechtige Orchestrator-Adresse: die Notiz haelt sie als Momentaufnahme — bewusste Abweichung vom Persistenz-Verzicht in `pane-start`; abgesichert durch die Pruefung aus Randfall 2. Begruendung in der Spec festhalten

---

**Erstellt mit:** `/dtb:feature-discover`
