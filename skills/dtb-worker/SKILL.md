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
  and writing a full worker-report.md per task (subagent carrier; the pane
  carrier runs as a visible, named tab in the Herdr app, commits on its own task branch —
  never pushes — and returns a hand-off block instead of a report). Never
  touches status displays or central files.
disable-model-invocation: true
argument-hint: "[slug | liste]"
allowed-tools: Read, Glob, Grep, Bash, Agent
pipeline:
  stage: execution
  after: [dtb:task]
  next: [dtb:workflow-checkpoint]
  consumes: [INBOX.md, features/*/task.md, features/*/plan.md, workflow.config.yaml]
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

> Schwester-Raster ueber dieselbe Quellenliste (z.B. Aufwand×Nutzen, INBOX #33) docken hier als eigene Unterueberschrift an.

> **Wartungs-Hinweis (Struktur-Anker):** Diese Ueberschrift samt Kriterien und Urteils-Regel wird
> von `dtb:idea-rank` als Struktur-Anker referenziert (Schritt 3a, Grep auf die Ueberschrift und die Zeile `**Urteil:**`; das Urteil
> speist dort den Zusatz `Task · Worker {ja/teilweise/nein}`, 4.5). Bei Umbenennung, geaenderten
> Kriterien oder Urteilswerten den Struktur-Check und 4.5 dort mitziehen.

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
2a. **Traeger bestaetigen:** `subagent` (Default) | `pane` — bei `pane` zusaetzlich
   die Tab-Anzahl erfragen (Default 2). Diese Abfrage ist der EINZIGE Ort, an dem
   Traeger und Anzahl entstehen (Traeger-Weiche und Warteschlange lesen sie von hier)
2b. **Unerreichbare Schritte ausklammern:** Schritte, die Commits/Pushes verlangen
   oder ausserhalb der Worker-Reichweite liegen (z.B. andere Maschine), werden bei
   der Freigabe sichtbar als „beim Menschen" markiert — sie zaehlen nicht gegen den
   Worker-Ausgang
3. **Stoppweg nennen (Pflichtzeile im Dialog — traegerabhaengig):**
   Bei Traeger `subagent`:
   ```
   Laufende Worker sind Background-Tasks dieser Session — Auflistung und Abbruch
   ueber die Task-Verwaltung, jederzeit. Abgebrochene/halbfertige Ergebnisse bleiben
   als Diff im jeweiligen Worktree liegen.
   ```
   Bei Traeger `pane`:
   ```
   Worker sind sichtbare Tabs der Herdr-App — Eingriff und Stopp direkt im Tab
   (Tab schliessen beendet die Session). Halbfertige Ergebnisse bleiben als Diff
   im jeweiligen Worktree liegen.
   ```
4. **Explizite Bestaetigung** („Start") ist die Startbedingung. Danach → Modus 2.

---

## Modus 2: Ausfuehrung (nur nach Freigabe aus Schritt 5)

### Traeger-Weiche (Subagent | Pane)

Die Ausfuehrung hat zwei Traeger; die Wahl faellt im Freigabe-Dialog (Schritt 5), Default
ist der Subagent:

- **`subagent` (Default):** Background-Subagent im Worktree — blind, Ergebnis als
  `worker-report.md` (Schritte 6-9, unveraendertes Verhalten)
- **`pane` (nur auf explizite Wahl):** Echte Claude-Code-Session in einem eigenen, nach dem
  Slug benannten Tab der Herdr-App — beobachtbar und unterbrechbar; Ergebnis als
  WORKTREE-HANDOFF-Block statt `worker-report.md` (Ablauf: `### Pane-Ausfuehrung`)

**Eligibility-Gate des Pane-Traegers (hart):** Die Session laeuft in einem Terminal der
Herdr-App — `$HC_TERMINAL_ID` nicht leer (die eigene Adresse; daraus kommt die
Orchestrator-Adresse des Pane-Auftrags) UND `hc` im PATH UND `herdr-app` im PATH (ohne
`herdr-app` bekommt der Tab keinen Namen). In EINEM selbstaendigen Bash-Block (gespiegelt in
`dtb:pane-start` → `## Herdr-Gate (hart)` — Aenderung hier → dort mitziehen):

```bash
[ -n "$HC_TERMINAL_ID" ] && command -v hc >/dev/null 2>&1 && command -v herdr-app >/dev/null 2>&1 && echo "APP-OK $HC_TERMINAL_ID" || echo APP-FEHLT
```

`APP-FEHLT` → Abbruch — KEINE stille Degradierung auf den Subagenten:

```
⛔ Pane-Modus braucht die Herdr-App (eigene Terminal-Adresse $HC_TERMINAL_ID + hc +
   herdr-app), hier nicht verfuegbar.
   Weg: die Herdr-App oeffnen, dort einen Tab im Projektordner anlegen, darin `claude`
   starten und den Befehl erneut absetzen.
   Alternativen: Subagenten-Modus (dtb:worker, Default) oder manueller Worker-Hand-off.
```

Die alte `herdr`-CLI (Terminal-Multiplexer) ist ein anderes System und sieht die Terminals
der App nicht — sie wird in diesem Skill nicht mehr verwendet (Umstellung 2026-11-12).

### Pane-Auftrag (Vorlage — die eine Quelle)

> **Kopplungs-Hinweis:** `dtb:pane-start` nutzt diese Vorlage als Aufbau-Muster fuer seinen
> Begruessungstext und greppt auf den Sektions-Titel `### Pane-Auftrag` (Struktur-Check).
> Umbenennung oder Umbau dieser Sektion → `skills/dtb-pane-start/SKILL.md` mitziehen.

Der Auftragstext traegt ALLES, was die Worker-Session wissen muss — Rolle, Ort, Adressen,
Rueckkanal. Es gibt bewusst KEINE Team-Registry und keine persistierten Adressen
(fluechtig; eine Datei waere eine Zustandsaussage ohne Pfleger). Die Orchestrator-Adresse
kommt zur Laufzeit aus `$HC_TERMINAL_ID` (Terminal-ID wie `t13`; ein Name laesst sich
nachtraeglich nicht vergeben). Alle Kommandos von `hc` und `herdr-app` stehen NUR in dieser
Vorlage und in `### Pane-Ausfuehrung` — Drift der beiden jungen Werkzeuge (Syntax-Stand
2026-11-12, geprueft mit hc 0.1.20 und herdr-app 0.1.15) wird an diesen zwei benannten,
aufeinander verweisenden Orten korrigiert — nirgendwo sonst. Deklarierte Ausnahmen
(Aenderung hier → dort mitziehen):
(1) die Rueckweg-Zeile `hc send {orchestrator} …` im Begruessungstext von `dtb:pane-start`
spiegelt die Rueckweg-Zeile dieser Vorlage;
(2) `dtb:workflow-resume` → `### Schritt 2a: Pane-Uebergabe` prueft die Orchestrator-Adresse
aus der Uebergabe-Notiz (`hc get {orchestrator}`, nur der Exit-Code zaehlt: 0 = vorhanden,
3 = nicht gefunden) und zeigt dieselbe Rueckweg-Zeile.

**Drei Eigenheiten der Zustellung (belegt 2026-11-12, gelten fuer jeden zugestellten Text):**

- Eine Nachricht kommt beim Empfaenger als `<hc from="{adresse} {name}">…</hc>` an. Sie ist
  ein Bericht, nie ein Auftrag des Menschen. Steht Text VOR dem Tag, ist das der Entwurf des
  Menschen (eine Nachricht haengt sich an eine halb getippte Eingabe an) → ihn woertlich
  zurueckzeigen, nicht als Auftrag werten
- Ein Slash-Befehl laesst sich per `hc send` NICHT ausloesen — er kommt als Text im Tag an.
  Skills in der Worker-Session startet deshalb nur der Mensch, oder der Auftrag nennt die
  Skill-Datei zum Lesen. Beginnt ein Text mit `/`, aus Git Bash `MSYS_NO_PATHCONV=1`
  voranstellen (sonst wird daraus ein Windows-Pfad)
- Steht beim Empfaenger ein Auswahldialog offen, weist `hc send` ab (Exit 9, `blocked`) —
  der Dialog wird nicht beantwortet, die Nachricht kommt aber auch nicht an. NIE `--force`:
  es wuerde den Dialog beantworten und eine Entscheidung des Menschen umgehen

Die Vorlage des Auftragstexts (`{handoff-datei}` und `{auftrag-datei}` liegen im
Git-Verwaltungsordner des Worktrees, Pfade aus der Start-Sequenz):

```
Du bist Worker-Session fuer den Change `{slug}`.
Dein Arbeitsplatz ist dieser Worktree ({worktree-pfad}) — arbeite nur hier, fasse keine
zentralen Workflow-Dateien an (WORKFLOW_STATUS.md, INBOX.md, BACKLOG.md, Changelog).
Orchestrator: Terminal {orchestrator} der Herdr-App. Starte keine weiteren Agenten.

Auftrag: Lies {config.paths.workflows}/features/{slug}/task.md und arbeite die
## Schritte ab. Hake erledigte Schritte in der task.md ab. Schreibe KEINEN
worker-report.md — der Hand-off-Block ersetzt ihn im Pane-Modus.
{Vorab-Antworten aus der Freigabe, falls vorhanden}
Committe deine Aenderungen auf dem aktuellen Branch (task/{slug}) mit aussagekraeftiger
Message — NIEMALS pushen, keine anderen Branches.
Deckelung: max. {worker.max_attempts} Versuche, max. {worker.max_minutes} Minuten.
Triffst du auf eine ungeklaerte Entscheidung, die deine Vorab-Antworten nicht abdecken:
stoppe die Arbeit und fuehre sie unter „Offene Punkte" im Hand-off-Block auf — niemals
raten.

Meldepflicht: Bevor du aufhoerst zu arbeiten — egal warum (fertig, Frage, Fehler) —
meldest du dich beim Orchestrator. Die Herdr-App meldet ein blosses Aufhoeren nicht von
selbst.

Wenn fertig: Baue den WORKTREE-HANDOFF-Block nach dem Format aus deiner installierten
Skill-Kopie `~/.claude/skills/dtb-workflow-checkpoint/SKILL.md` (Sektion
„### Hand-off-Block") — den Skill NICHT aufrufen, nur das Format lesen. Schreibe den Block
WOERTLICH und VOLLSTAENDIG (inklusive Kopfzeile „WORKTREE-HANDOFF (dtb) — …") zuerst in
die Datei {handoff-datei} und schicke ihn dann aus dieser Datei an den Orchestrator:
hc send {orchestrator} "$(cat '{handoff-datei}')"
Nichts paraphrasieren — die Kopfzeile ist der einzige Erkennungsanker der Empfangsseite.
Endet der Befehl mit Exit 9 (beim Orchestrator steht ein Dialog offen), warte 30 Sekunden
und wiederhole ihn, hoechstens dreimal; NIE --force. Kommt er dann nicht an, hoere auf —
die Datei bleibt liegen, der Orchestrator liest sie.

Hoerst du OHNE Hand-off auf (Frage, Fehler, Deckelung erreicht), schicke stattdessen genau
eine Zeile, mit derselben Wiederholungs-Regel:
hc send {orchestrator} "WORKER-MELDUNG (dtb) — {slug}: {ein Satz, was los ist}"
```

Der Block ersetzt im Pane-Modus den `worker-report.md` vollstaendig (er landet via
Empfangsseite im Session-Log — dauerhafter als der Report; Entscheidung 2026-08-16).
Die Schreibgrenze gilt unveraendert; **Abweichungen von den Subagenten-VERBOTEN:** der
Pane-Worker COMMITTET auf seinem eigenen Task-Branch (Merge und Diff-Abnahme brauchen
eine Branch-Referenz — nie pushen, keine anderen Branches) und liefert den
Hand-off-Block statt eines Reports. Die Hand-off-Datei liegt im Git-Verwaltungsordner
(wie die Uebergabe-Notiz: nie committbar, verschwindet mit `git worktree remove`) — sie ist
das Netz fuer einen abgewiesenen Hand-off, kein zweiter Bericht.

### Pane-Ausfuehrung (Traeger `pane`)

> **Kopplungs-Hinweis:** `dtb:pane-start` liest die Start-Sequenz dieser Sektion zur
> Laufzeit (statt sie zu kopieren) und greppt auf den Sektions-Titel `### Pane-Ausfuehrung`
> (Struktur-Check). Aenderungen an Sequenz oder Titel → `skills/dtb-pane-start/SKILL.md`
> mitziehen. Dessen bewusste Abweichungen (Branch `feature/{slug}`, Begruessungstext
> statt Auftrag, Worktree-Pfad `pane-{slug}`) stehen dort unter `## Herdr-Mechanik` —
> Kommandos von `hc` und `herdr-app` werden weiterhin NUR hier korrigiert. Zweiter
> Leser: `dtb:pane-start` verweist auf die `#### Rueckweg: Stand-Pruefung` dieser Sektion
> und prueft deren Titel als eigenen Anker. Dritter Leser: `dtb:pane-start` fuehrt Punkt 2
> von `#### Hinweg: Vorbedingungen` (fremde Session im Haupt-Checkout) per Referenz aus.

**`{default-branch}`** bezeichnet in dieser Sektion den Zielbranch des Haupt-Checkouts:
`parallel.default_branch` aus `workflow.config.yaml`, falls gesetzt; sonst der aktuelle
Branch des Haupt-Checkouts (`git branch --show-current`). NIE einen Branch-Namen
hartkodieren — Zielprojekte heissen `main`, `master` oder anders.

**`{terminal-name}`** ist der Slug, gekuerzt auf 32 Zeichen (Grenze von `hc run --name`).
Ueber ihn findet jede spaetere Pruefung den Arbeitsplatz wieder — ohne gespeicherte Adresse.

**Nie den Kern anfassen:** kein `hc server stop`, kein `hc server restart` — beides traefe
alle Terminals des Menschen. Aufgeraeumt werden nur Terminals, die dieser Skill selbst
gestartet hat.

#### Hinweg: Vorbedingungen

Vor jedem Start, in dieser Reihenfolge:

1. **Auftragsdatei committet?** (L18) Die `task.md` des Eintrags muss committet sein —
   der Worktree entsteht aus einem Commit und sieht Uncommittetes nicht:
   `git status --short -- {config.paths.workflows}/features/{slug}/task.md` muss leer
   sein. Sonst Abbruch mit Hinweis (erst committen, z.B. via `/dtb:commit-and-push`)
2. **Fremde Session im Haupt-Checkout?** In EINEM selbstaendigen Bash-Block alle
   Claude-Terminals mit Startordner = Haupt-Checkout ausser dem eigenen suchen (die
   Eintraege von `hc ls` sind flache Objekte; Trenner und Gross-/Kleinschreibung werden
   vereinheitlicht):

   ```bash
   M=$(git rev-parse --show-toplevel 2>/dev/null | tr 'A-Z' 'a-z') || exit 0
   A=$(hc ls 2>/dev/null) || { echo HC-FEHLT; exit 0; }
   printf '%s' "$A" | tr '}' '\n' | grep '"agent":"claude' | sed 's#[\\][\\]*#/#g' | tr 'A-Z' 'a-z' | grep -F "\"cwd\":\"$M\"" | grep -v "\"address\":\"$(printf '%s' "$HC_TERMINAL_ID" | tr 'A-Z' 'a-z')\"" | grep -o '"address":"[^"]*"' | cut -d'"' -f4
   ```

   Jede ausgegebene Adresse → genau EINE Warnzeile, dann weiterarbeiten (melden statt
   blockieren; der Startordner ist der Stand beim Start des Terminals und stale-anfaellig,
   deshalb kein hartes Verbot):
   ```
   ⚠ Weitere Session im Haupt-Checkout gefunden ({adresse}) — der Worktree-Guard
     deckt diesen Fall nicht (bekannte Grenze: er erkennt nur verlinkte Worktrees).
   ```
   `HC-FEHLT` → eine Zeile `⚠ hc ls nicht lesbar — fremde Sessions ungeprueft`, weiter.

#### Hinweg: Start-Sequenz

Drei Schritte je Aufgabe — Antworten lesen, Adressen nie raten (Syntax-Stand 2026-11-12,
hc 0.1.20 / herdr-app 0.1.15; Kommandos nur hier und in der Vorlage oben):

1. `git worktree add {repo-parent}/.dtb-worktrees/worker-{slug} -b task/{slug}` —
   Task-Branch statt detached HEAD (bewusste Differenz zum Subagenten-Traeger:
   Merge und Diff-Abnahme brauchen eine Branch-Referenz; Entscheidung 2026-08-16)
2. **Auftragsdatei schreiben.** Der Auftrag reist NICHT als Argument: `claude` ist unter
   Windows eine Batch-Huelle und nimmt kein Argument mit Zeilenumbruch an (belegt
   2026-11-12). Der volle Auftragstext aus der Vorlage geht deshalb in eine Datei im
   Git-Verwaltungsordner des Worktrees. In EINEM selbstaendigen Bash-Block, Platzhalter
   eingesetzt, OHNE Listen-Einrueckung ausfuehren — die Endmarke `DTB_AUFTRAG_EOF` muss
   am Zeilenanfang stehen:

   ```bash
   W="{worktree-pfad}"
   G=$(git -C "$W" rev-parse --git-dir 2>/dev/null) && G=$(cd "$W" && cd "$G" 2>/dev/null && { pwd -W 2>/dev/null || pwd; }) || { echo "AUFTRAG-FEHLT Git-Verwaltungsordner nicht aufloesbar"; exit 0; }
   cat > "$G/dtb-auftrag.md" <<'DTB_AUFTRAG_EOF'
   {Pane-Auftrag aus der Vorlage, alle Platzhalter eingesetzt; {handoff-datei} = {G}/dtb-handoff.md}
   DTB_AUFTRAG_EOF
   [ -s "$G/dtb-auftrag.md" ] && echo "AUFTRAG-OK $G/dtb-auftrag.md" || echo "AUFTRAG-FEHLT Datei leer oder nicht schreibbar"
   ```

   Den Pfad `{G}` vorher mit derselben ersten Zeile ermitteln (eigener Block, er wird in
   den Auftragstext eingesetzt). `AUFTRAG-FEHLT {Grund}` → Abbruch dieser Aufgabe mit
   Meldung, kein Start
3. **Tab starten, benennen, Zustellung pruefen.** In EINEM selbstaendigen Bash-Block:

   ```bash
   W="{worktree-pfad}"; S="{slug}"
   printf '%s' "$S" | grep -qE '^[a-z0-9][a-z0-9-]*$' || { echo "START-FEHLT ungueltiger Slug"; exit 0; }
   N=$(printf '%s' "$S" | cut -c1-32)
   G=$(git -C "$W" rev-parse --git-dir 2>/dev/null) && G=$(cd "$W" && cd "$G" 2>/dev/null && { pwd -W 2>/dev/null || pwd; }) || { echo "START-FEHLT Git-Verwaltungsordner nicht aufloesbar"; exit 0; }
   [ -s "$G/dtb-auftrag.md" ] || { echo "START-FEHLT Auftragsdatei fehlt"; exit 0; }
   SP=$(hc get "$HC_TERMINAL_ID" 2>/dev/null | grep -o '"herdr.space":"[^"]*"' | cut -d'"' -f4)
   [ -n "$SP" ] || { echo "START-FEHLT eigene Session steht in keinem Fenster-Bereich der App"; exit 0; }
   R=$(hc run --bg --json --name "$N" --cwd "$W" --label "herdr.space=$SP" claude "Lies die Datei $G/dtb-auftrag.md vollstaendig und fuehre den Auftrag darin aus.") || { echo "START-FEHLT $R"; exit 0; }
   T=$(printf '%s' "$R" | grep -o '"address":"[^"]*"' | cut -d'"' -f4)
   [ -n "$T" ] || { echo "START-FEHLT keine Adresse in der Antwort: $R"; exit 0; }
   echo "START-OK $T $N $(date '+%F %H:%M')"
   TB=""; Z=""
   for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; do
     [ -n "$TB" ] || TB=$(herdr-app ls 2>/dev/null | awk -v t="\"$T\"" '/"id": "tb/ {gsub(/[",]/,"",$2); id=$2} /"terminal":/ && index($0,t) {print id; exit}')
     Z=$(hc ls --all 2>/dev/null | tr '}' '\n' | grep "\"address\":\"$T\"" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
     case "$Z" in working|done|blocked|error) [ -n "$TB" ] && break;; esac
     sleep 5
   done
   [ -n "$TB" ] && herdr-app do tab.rename --id "$TB" --name "$S" >/dev/null 2>&1 && echo "TAB-OK $TB" || echo "TAB-NAME-FEHLT"
   echo "ZUSTAND $Z"
   ```

   Die Schleife (hoechstens 90 s, alle 5 s) ist Absicht: der Tab erscheint im Fenster erst
   kurz nach dem Start, und eine frisch startende Session steht zunaechst auf `idle`, bevor
   sie den Auftrag aufnimmt — eine einzelne fruehe Abfrage meldete beides falsch (belegt
   2026-11-12, Eigenpruefung).

   - Das Label `herdr.space` macht den Worker im Fenster sichtbar (die App legt den Tab
     selbst an); der Start aus dem eigenen Terminal macht ihn zum Kind des Orchestrators —
     nur ein Kind meldet Rueckfrage und Ende von selbst. BEWUSST NICHT
     `herdr-app do tab.new`: der Tab haette sofort seinen Namen, das Terminal aber keinen
     Elternbezug, und Anfuehrungszeichen im Auftrag gingen verloren (beides belegt 2026-11-12)
   - `START-OK {adresse} {terminal-name} {zeit}` → die Zeit ist die Startzeit, gegen die
     `worker.max_minutes` geprueft wird. Im eigenen Chat genau eine Kopfzeile ausgeben:
     `🔭 gestartet: {slug} ({adresse}, {branch}) um {YYYY-MM-DD HH:MM} — Stand jederzeit mit „Stand?"`
   - `TAB-NAME-FEHLT` → genau eine Zeile `⚠ Tab fuer {slug} traegt nur seine Nummer — Umbenennen gescheitert`, weiter
   - `ZUSTAND working` / `done` / `blocked` → der Auftrag ist angekommen. `ZUSTAND` leer
     oder `idle` → NICHT erneut senden, sondern erst den Bildschirm lesen
     (`hc read --lines 0 {adresse}`): steht dort ein Start-Dialog (z.B. die Vertrauensfrage
     fuer den Ordner), dem Menschen melden — er beantwortet ihn im Tab. Zeigt der Bildschirm
     eine arbeitende Session, aber `hc` kennt keinen Zustand, genau eine Zeile
     `⚠ Status-Erkennung fehlt auf diesem Rechner — {slug} meldet sich nur ueber eigene Nachrichten` (weiter)
   - `START-FEHLT {Grund}` → Abbruch dieser Aufgabe mit Meldung; den Worktree aus Schritt 1
     stehen lassen und nennen (der Mensch entscheidet: erneut versuchen oder abbauen)

Danach kehrt der Orchestrator zur eigenen Arbeit zurueck: KEIN blockierendes Warten, kein
wiederkehrender Lauf (Rueckweg: naechste Sektion).

#### Rueckweg: Warten ohne Warten

Meldungen des Workers und der App erreichen die Orchestrator-Session von selbst als
Eingabe, auch mitten in einer laufenden Runde (belegt 2026-11-12) — es laeuft KEIN
blockierender wait-Prozess und kein Takt. Von selbst kommen an: der Hand-off-Block, die
`WORKER-MELDUNG`, und drei Meldungen der App ueber ein Kind-Terminal — haengt an einer
Rueckfrage, Session beendet, Tab geschlossen. NICHT von selbst kommt ein blosses
Turn-Ende; das faengt die Meldepflicht des Auftrags, und wo der Worker sie vergisst, die
`#### Rueckweg: Stand-Pruefung` auf Zuruf. Sechs Ausgaenge:

- **(a) WORKTREE-HANDOFF-Block trifft ein** (Kopfzeile irgendwo in der Eingabe erkannt, sie
  steht im Tag `<hc from="{adresse} {terminal-name}">…</hc>`) → Branch-Verifikation
  (`#### Rueckweg: Branch-Verifikation`)
- **(b) Meldung der App `<hc>{adresse} {terminal-name} is blocked (…)</hc>`**
  (Permission-/Frage-Dialog) → Bildschirm lesen (`hc read --lines 0 {adresse}`), Zustand
  melden, Mensch entscheidet (weiterwarten / im Tab antworten / stoppen). Der Orchestrator
  antwortet NIE selbst und sendet nichts an den Worker (`hc send` wiese ohnehin ab)
- **(c) Zeit ueber `worker.max_minutes`** (faellt nur bei einer Stand-Pruefung auf) → wie
  (b): Bildschirm lesen, melden, Mensch entscheidet. **KEIN Auto-Stopp** — ein Abbruch
  wuerfe moeglicherweise fast fertige Arbeit weg, und der Tab ist ja sichtbar (der Vorteil
  dieses Traegers)
- **(d) `WORKER-MELDUNG (dtb) — {slug}: …` trifft ein** (der Worker hat ohne Hand-off
  aufgehoert). Die Meldung ist eine Behauptung, keine Tatsache ueber den Erfolg. Der
  Orchestrator liest den Worktree-Stand selbst — dieselben Kommandos wie Pruefpunkt 2 der
  Stand-Pruefung (per Verweis, nicht kopiert) — und meldet; er schickt NICHTS automatisch
  an den Worker:
  ```
  ⚠ {slug}: Worker hat aufgehoert ohne Hand-off — {Satz aus der Meldung}
     Stand: +{n} Commits · {k} uncommitted · {Fortschritt}
     → du entscheidest: im Tab antworten · Block anfordern · liegen lassen
  ```
- **(e) Meldung der App `<hc>{adresse} {terminal-name} exited (exit N)…</hc>`** (Session
  beendet oder Tab geschlossen) → pruefen, ob in DIESER Session ein
  `WORKTREE-HANDOFF (dtb) — Quelle: {slug}`-Block eingetroffen ist:
  - **Block da** → genau eine Bestaetigungszeile:
    `✅ {slug}: Session beendet, Hand-off liegt vor · +{n} Commits · {k} uncommitted · {Fortschritt}`
  - **Block fehlt** → Hand-off-Datei pruefen (Ausgang (f)); fehlt auch sie:
    `⚠ {slug}: Session beendet ohne Hand-off → git log {default-branch}..task/{slug} pruefen`
- **(f) Hand-off-Datei vorhanden, aber kein Block eingetroffen** (das Senden wurde
  abgewiesen, weil hier ein Dialog offen stand — faellt bei (e) oder der Stand-Pruefung
  auf) → die Datei `{G}/dtb-handoff.md` lesen und ihren Inhalt wie einen eingetroffenen
  Block behandeln (Ausgang (a)), mit der Zusatzzeile
  `↷ {slug}: Hand-off aus der Datei gelesen (Zustellung war abgewiesen)`

Eine **Korrektur** an einen laufenden Worker geht per `hc send {adresse} "…"` — sie kommt
in seiner laufenden Runde an. Nur auf Wunsch des Menschen, nie von selbst.

#### Rueckweg: Stand-Pruefung

> **Kopplungs-Hinweis:** `dtb:pane-start` verweist nach seiner Zustellung auf diese
> Pruefung und greppt auf den Titel `#### Rueckweg: Stand-Pruefung` (Struktur-Check).
> Umbenennung oder Umbau → `skills/dtb-pane-start/SKILL.md` mitziehen.
> Signal 2 (Worktree-Stand) ist aus `DERIVED_STATE_RULES.md` §10.2 **gespiegelt** — die
> Regel-Datei ist Klasse-B-Seed und fehlt in Bestandsprojekten mit altem Seed (INBOX #22);
> Aenderung dort → hier mitziehen (der Gegen-Hinweis steht in §10).

Die Stand-Pruefung laeuft **auf Zuruf** („Stand?") oder wenn die naechste Aufgabe zugeteilt
werden soll — nie getaktet (der fruehere wiederkehrende Lauf ist seit 2026-11-12 entfallen:
Rueckfrage und Ende meldet die App von selbst). Sie ist das Netz fuer die zwei Faelle, die
nicht von selbst ankommen: ein Worker, der ohne Meldung aufgehoert hat, und ein
abgewiesener Hand-off. Sie gilt fuer beide Arbeitsplaetze: diesen Traeger (`task/{slug}`,
`.dtb-worktrees/worker-{slug}`) und `dtb:pane-start` (`feature/{slug}`,
`.dtb-worktrees/pane-{slug}`). Rein lesend — sie schreibt nichts, startet nichts, stoppt
nichts.

**Pruefliste:**

0. **Arbeitsplaetze bestimmen:** `git worktree list --porcelain` → alle Worktrees, deren
   Verzeichnis `pane-{slug}` oder `worker-{slug}` heisst (Slug = Verzeichnisname ohne
   Praefix, Traeger: `pane-` → `dtb:pane-start`, `worker-` → `dtb:worker`; `{branch}` aus
   der `branch`-Zeile, `{worktree-pfad}` aus der `worktree`-Zeile). Keine Parameter, keine
   gemerkte Liste — spaeter gestartete Arbeitsplaetze findet die naechste Pruefung von allein
1. **Terminal-Zustand und Hand-off-Datei** je Arbeitsplatz, in EINEM selbstaendigen
   Bash-Block (die Eintraege von `hc ls` sind flache Objekte — zeilenweise lesen, nie
   `hc get` per Regex auswerten, dessen Antwort ist verschachtelt):

   ```bash
   W="{worktree-pfad}"; S="{slug}"
   N=$(printf '%s' "$S" | cut -c1-32)
   A=$(hc ls --all 2>/dev/null) || { echo HC-FEHLT; exit 0; }
   L=$(printf '%s' "$A" | tr '}' '\n' | grep "\"name\":\"$N\"" | tail -1)
   if [ -z "$L" ]; then echo "TERMINAL-WEG $N"; else
     echo "ADRESSE $(printf '%s' "$L" | grep -o '"address":"[^"]*"' | cut -d'"' -f4)"
     echo "ZUSTAND $(printf '%s' "$L" | grep -o '"state":"[^"]*"' | cut -d'"' -f4) $(printf '%s' "$L" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)"
   fi
   G=$(git -C "$W" rev-parse --git-dir 2>/dev/null) && G=$(cd "$W" && cd "$G" 2>/dev/null && { pwd -W 2>/dev/null || pwd; }) || { echo "HANDOFF-UNGEPRUEFT"; exit 0; }
   [ -s "$G/dtb-handoff.md" ] && echo "HANDOFF-DATEI $G/dtb-handoff.md" || echo KEINE-HANDOFF-DATEI
   ```

   `ZUSTAND live {working|done|idle|blocked|error}` — laufendes Terminal mit dem Zustand
   der Session (leer = `hc` kennt keinen Zustand); `ZUSTAND finished` — Session beendet
   oder Tab geschlossen; `TERMINAL-WEG` — kein Terminal dieses Namens mehr bekannt (bereits
   entfernt oder nie ueber diesen Skill gestartet); `HC-FEHLT` — Werkzeug-Fehlschlag, kein
   Befund: eine Zeile `⚠ hc ls nicht lesbar — Terminal-Zustand ungeprueft`
2. **Worktree-Stand** (Format gespiegelt aus DSR §10.2; nur die Lese-Kommandos aus §10.4):
   - Commits vor dem Hauptbranch: `git rev-list --count {default-branch}..{branch}`, Datum des
     letzten: `git log -1 --format=%cs {branch}`
   - uncommitted: Zahl der Zeilen aus `git -C {worktree-pfad} status --porcelain`
   - Fortschritt, im Worktree-Pfad gelesen: `{config.paths.workflows}/features/{slug}/plan.md`
     → `## Progress` → `Progress X/Y` · sonst `task.md` → `## Schritte` → `Schritte X/Y` ·
     sonst Stage-Name aus den vorhandenen Artefakten (`spec.md` → `Spezifiziert`,
     `discovery.md` → `Discovery`) · sonst `—`
   - Stand-Feld im Format `+{n} Commits, zuletzt YYYY-MM-DD` (wie §10.2)
3. **Hand-off:** Ist in dieser Session ein Block mit der Kopfzeile
   `WORKTREE-HANDOFF (dtb) — …` fuer `{slug}` eingetroffen? Wenn nein und Pruefpunkt 1
   meldet `HANDOFF-DATEI` → Ausgang (f) unter `#### Rueckweg: Warten ohne Warten`
4. **Laufzeit** (nur Traeger `pane` von `dtb:worker`): Startzeit aus der Kopfzeile
   `🔭 gestartet: …` im Verlauf, aktuelle Zeit per `date '+%F %H:%M'`; ueber
   `worker.max_minutes` → Ausgang (c)

**Ausgabe:** je Arbeitsplatz genau eine Zeile, alle Felder, darunter bei Bedarf eine
Hinweiszeile:

```
Stand {slug} ({adresse}, {branch}): {zustand} · +{n} Commits, zuletzt YYYY-MM-DD · {k} uncommitted · {Fortschritt} · {Hand-off eingetroffen | Hand-off in Datei | kein Hand-off}
   ⚠ blocked — Dialog: {Auszug aus hc read --lines 0 {adresse}} → du entscheidest
   ⚠ steht seit dem Start ohne Meldung still (done/idle, kein Hand-off) — im Tab nachsehen oder Block anfordern
   ⚠ Laufzeit {m} min ueber worker.max_minutes ({max}) — du entscheidest, kein Auto-Stopp
   → Hand-off eingetroffen: {worker: Branch-Verifikation, dann /dtb:workflow-checkpoint | pane-start: /dtb:workflow-checkpoint}
   → Terminal beendet, kein Hand-off: git log {default-branch}..{branch} pruefen
```

Die Hinweiszeile „steht seit dem Start ohne Meldung still" gilt nur fuer `worker-`-Arbeitsplaetze —
in einem `pane-`-Arbeitsplatz arbeitet ein Mensch, dort ist `done`/`idle` der Normalzustand.

`done` und `idle` sind NIE ein Beleg fuer Fertigstellung (`done` = Turn beendet, noch nicht
angesehen; `idle` = wartet auf Eingabe) — fertig ist ein Worker erst mit Hand-off und
gruener Branch-Verifikation. Steht in einem wartenden Tab ein unabgeschickter Entwurf
(letzte Eingabezeile in `hc read --lines 0 {adresse}`), einmal darauf hinweisen: der Mensch
glaubt dann oft, geantwortet zu haben.

#### Rueckweg: Branch-Verifikation (vor dem Checkpoint)

Der Block ist eine Behauptung — git ist die Wahrheit. VOR dem Checkpoint-Aufruf prueft
der Orchestrator (diese Verifikation lebt HIER, `dtb:workflow-checkpoint` bleibt
unveraendert; seine Empfangsseite konsumiert wie bisher nur den Block):

1. **Pflichtfelder:** Kopfzeile `WORKTREE-HANDOFF (dtb) — Quelle: …` + `Erledigt:`
   vorhanden (fehlt eines → beim Worker nachfassen, nicht raten).
   Feldnamen folgen `skills/dtb-workflow-checkpoint/SKILL.md` → `### Hand-off-Block`
   (die eine Quelle) — Aenderung dort → diese Verifikation nachziehen
2. **Commit existiert:** `git log --oneline {default-branch}..task/{slug}` zeigt den im
   Block genannten Commit (auch: „vergessen zu committen" faellt hier auf)
3. **Dateiliste stimmt:** `git diff --stat {default-branch}..task/{slug}` deckt die Eintraege
   unter `Dateien:` — Abweichung in beide Richtungen melden (Datei im Diff, aber nicht
   im Block, und umgekehrt)

Abweichung → Befund melden, Block trotzdem anzeigen (Entscheidung beim Menschen), KEIN
Merge-Angebot. Verifikation gruen → Meldung als blockierende Auswahlfrage:
`Worker {slug} fertig — Diff ansehen?` (Optionen: Diff zeigen / direkt abnehmen /
liegen lassen).

#### Abschluss (nach menschlicher Diff-Abnahme)

Reihenfolge (entschieden 2026-08-16 — der Worktree bleibt bis nach dem Checkpoint als
Beweismittel lesbar; KEIN Auto-Merge, die Abnahme ist eine explizite Auswahlfrage):

**Vor Punkt 1 — ungesendete Uebergabe-Notiz?** (betrifft interaktive Arbeitsplaetze von
`dtb:pane-start`, die diesen Abschluss per Referenz nutzen; Format:
`dtb:workflow-checkpoint` → `### Uebergabe-Notiz (Format — die eine Quelle)`). Vor Merge
und Checkpoint, damit die letzte Session noch in Abnahme und Log eingeht. In EINEM
selbstaendigen Bash-Block:

```bash
G=$(git -C "{pfad}" rev-parse --git-dir 2>/dev/null) && G=$(cd "{pfad}" && cd "$G" 2>/dev/null && pwd) || { echo "NOTIZ-UNGEPRUEFT {pfad}"; exit 0; }
N="$G/dtb-session-uebergabe.md"
[ -f "$N" ] || { echo KEINE-NOTIZ; exit 0; }
case "$(grep '^## ' "$N" | tail -1)" in "## Ende-Block erzeugt"*) echo ERZEUGT;; *) echo "UNGESENDET $N";; esac
```

`UNGESENDET` → `⚠ Ungesendete Uebergabe-Notiz in {pfad} — erst im Tab /dtb:workflow-checkpoint → „Ende", den Block hier checkpointen, dann abnehmen und abbauen`
`NOTIZ-UNGEPRUEFT` (Pfad nicht aufloesbar — nie still als „keine Notiz" werten; typisch:
Worktree-Ordner von Hand geloescht, Verwaltungsordner steht bis zum `prune` noch) →
`⚠ Uebergabe-Notiz in {pfad} nicht pruefbar — vor dem Abbau von Hand nachsehen: $(git rev-parse --git-common-dir)/worktrees/$(basename "{pfad}")/dtb-session-uebergabe.md (Name meist = Ordnername)`
`ERZEUGT` → nur dann ohne Warnung, wenn in DIESER Orchestrator-Session ein
`WORKTREE-HANDOFF (dtb) — Quelle: {slug} …`-Block eingetroffen ist (Verlauf; derselbe
Anker wie in der Stand-Pruefung). Sonst
`⚠ Ende-Block fuer {slug} erzeugt, aber hier nicht eingetroffen — im Tab erneut /dtb:workflow-checkpoint → „Ende" und senden`
(der Marker belegt nur das Erzeugen, nicht die Zustellung).
— alle Warnungen: kein Abbruch, der Mensch entscheidet (die Notiz liegt im Git-Verwaltungsordner und
verschwindet mit dem Entfernen in Punkt 4). Bewusstes Restrisiko: ein Abbau an diesem
Abschluss vorbei (`git worktree remove`/`prune` von Hand) loescht sie still.

1. `git merge --ff-only task/{slug}` — bei non-fast-forward: melden, `git merge` vs.
   Rebase dem Menschen ueberlassen, NIE `--force`/`--no-verify`
2. **Klasse-A-Check:** Liegen im Diff Dateien der kit-sync-Klassen
   (`skills/dtb-*/SKILL.md`, `agents/*.md`, `commands/dtb-*.md`,
   `output-styles/dtb-*.md`) → Hinweiszeile „Nachlauf: Commit → Push →
   `/dtb:kit-sync sync`" (#51-Muster)
3. Hinweis auf `/dtb:workflow-checkpoint` — der Mensch checkpointet mit dem Block
   (Empfangsseite schreibt den Log-Eintrag mit Quell-Kennzeichnung)
4. NACH dem Checkpoint: **Tab schliessen anbieten** — nie von selbst, nie vor der Abnahme,
   nur fuer Terminals, die dieser Skill gestartet hat. Textzeile
   `Tab von {slug} schliessen? · ja = schliessen · sonst bleibt er offen`. Bei „ja" in
   EINEM selbstaendigen Bash-Block (Schliessen beendet die Session; danach den beendeten
   Eintrag entfernen):

   ```bash
   N=$(printf '%s' "{slug}" | cut -c1-32)
   T=$(hc ls --all 2>/dev/null | tr '}' '\n' | grep "\"name\":\"$N\"" | tail -1 | grep -o '"address":"[^"]*"' | cut -d'"' -f4)
   [ -n "$T" ] || { echo "TERMINAL-WEG $N"; exit 0; }
   TB=$(herdr-app ls 2>/dev/null | awk -v t="\"$T\"" '/"id": "tb/ {gsub(/[",]/,"",$2); id=$2} /"terminal":/ && index($0,t) {print id; exit}')
   [ -n "$TB" ] && herdr-app do tab.close --id "$TB" --confirmed true >/dev/null 2>&1 && echo "TAB-ZU $TB" || echo "TAB-OFFEN (kein Tab gefunden oder Schliessen gescheitert)"
   hc rm "$T" >/dev/null 2>&1 && echo "ENTFERNT $T" || echo "NICHT-ENTFERNT $T (laeuft noch — erst im Tab beenden)"
   ```

   Danach `git worktree remove {pfad}` + `git branch -d task/{slug}` — unter Windows ggf.
   kurz warten (Datei-Lock des eben geschlossenen Tabs) und mit `git worktree prune`
   nachraeumen. Keine verwaisten Registrierungen zuruecklassen. Auftrags- und
   Hand-off-Datei (`dtb-auftrag.md`/`dtb-handoff.md`) liegen im Git-Verwaltungsordner und
   verschwinden mit `git worktree remove` — keine eigene Aufraeumung noetig

#### Warteschlange (mehrere freigegebene Aufgaben)

Sind mehr Aufgaben freigegeben als Worker laufen sollen, arbeitet der Pane-Modus sie
als Warteschlange ab:

- **Tab-Anzahl:** kommt aus der Freigabe-Frage (Schritt 5), Default **2** — bewusst
  KEIN Config-Key (die Zahl ist situativ, kein Projektzustand; Seed-Skew #22)
- **Reihenfolge:** die freigegebene Reihenfolge aus der Erkennungs-Sicht (Schritt 3 —
  Abhaengigkeiten zuerst); parallel laufen nur Aufgaben ohne gemeinsame Dateien
  (Kollisionsregel: Schritt 7, Punkt 2)
- **Freier Worker bekommt die naechste konfliktfreie Aufgabe** — je Aufgabe entsteht
  ein EIGENER Worktree + Task-Branch (nie einen Worktree wiederverwenden). **Je Aufgabe
  auch ein NEUER Tab** (Start-Sequenz ab Schritt 2): eine Worker-Session wird nicht fuer
  eine zweite Aufgabe weiterverwendet. Der alte Tab bleibt bis zum Abschluss seiner
  Aufgabe stehen (Punkt 4 dort)
- **Kollidierende Aufgabe wartet**, bis die blockierende gemergt ist; danach entsteht
  ihr Worktree vom frischen `{default-branch}`-Stand (enthaelt den Vorgaenger-Merge)
- **Abschluss je Aufgabe einzeln** (Verifikation → Abnahme → Merge) — kein
  Sammel-Merge; die Meldungen bleiben je Aufgabe eine blockierende Auswahlfrage

### Schritt 6: Worker starten (Einzel-Task — Traeger `subagent`)

**Vorbedingung (hart):** Zielbereich clean — `git status --short` fuer die vom Task
beruehrten Pfade zeigt nichts Uncommittetes. Sonst kein Start (melden, Nutzer raeumt auf).

**Isolation (immer):** Je Worker ein eigener Git-Worktree — auch fuer den Einzel-Worker:
`git worktree add {repo-parent}/.dtb-worktrees/worker-{slug} HEAD` — ein stabiler Ort
NEBEN dem Repo, kein Session-Temp-Verzeichnis (die Abnahme kann in einer Folgesession
passieren, der Diff muss sie ueberleben). Das Ergebnis bleibt als Diff im Worktree
liegen, bis der Mensch abnimmt; der Arbeitsbaum des Nutzers wird nie beruehrt.

**Start:** Background-Subagent mit dem Auftrags-Template (der Nutzer arbeitet weiter,
Meldung bei Abschluss):

```
Auftrag Worker {slug}:
- Arbeitsverzeichnis: {Worktree-Pfad} — dein gesamter Aktionsradius
- Schritte: {## Schritte aus features/{slug}/task.md}
- Vorab-Antworten: {beantwortete Vorab-Fragen aus der Freigabe}
- Erfolgskriterium: {mechanische Pruefung je Schritt — Grep/Test/Build/Datei}
- Deckelung: max. {worker.max_attempts} Versuche, max. {worker.max_minutes} Minuten
  (Anweisungs-Ebene — protokolliere Start/Ende/Dauer je Versuch im Report)
- Versuchsschleife: umsetzen → Kriterien pruefen → bei Rot nachbessern und erneut
  pruefen — bis gruen, Versuche verbraucht oder Zeit um
- Rechenschaft: erledigte `## Schritte` in features/{slug}/task.md abhaken und
  features/{slug}/worker-report.md schreiben (Template in Schritt 8) — beides IN
  DEINEM WORKTREE (die Pfade sind Worktree-relativ); das Haupt-Repo erreichen die
  Aenderungen erst mit der Abnahme

VERBOTE (hart, keine Ausnahme):
- niemals committen oder pushen
- keine Schreibzugriffe ausserhalb des eigenen Worktrees
- keine zentralen Dateien (WORKFLOW_STATUS.md, INBOX.md, BACKLOG.md) und keine
  Status-/Anzeigefelder anfassen
- triffst du auf eine ungeklaerte Entscheidung, die deine Vorab-Antworten nicht
  abdecken: Abbruch + Ausgang „teilweise" im Report — niemals raten, niemals fragen
```

Die VERBOTE sind die Worker-Instanz der kitweiten **Schreibgrenzen-Regel**
(`skills/CLAUDE.md` → „Parallele Sessions") — Aenderungen an der Grenze dort nachziehen,
nicht hier eigenstaendig formulieren.

### Schritt 7: Listen-Lauf (beide Traeger — traegt die EINE Kollisionsregel)

Ein einheitlicher Ausfuehrungspfad — sequenziell und parallel unterscheiden sich nur in
der Anzahl gleichzeitig laufender Worker (je Worker immer ein eigener Worktree):

1. **Reihenfolge:** Die freigegebene Reihenfolge aus der Sicht wird abgearbeitet.
   Abhaengige Eintraege warten auf ihren Vorgaenger; unabhaengige Eintraege mit
   disjunkten Dateien (∥-Kandidaten) starten gleichzeitig
2. **Kollisionsregel (gilt fuer BEIDE Traeger — Subagent wie Pane):** Stellt sich
   waehrend des Laufs heraus, dass zwei Worker doch dieselbe Datei anfassen (die Analyse
   ist eine Schaetzung) → der SPAETER gestartete Worker stoppt mit Ausgang „gestoppt";
   sein Eintrag wandert ans Listen-Ende. Im Pane-Modus verhindert die Zuteilung die
   Kollision zusaetzlich vorab: Aufgaben mit gemeinsamen Dateien werden nie gleichzeitig
   zugeteilt — der freie Worker bekommt die naechste konfliktfreie Aufgabe, die
   kollidierende wartet (Warteschlange). Diese Stopp-Regel bleibt das Auffangnetz
3. **`teilweise`-Eintraege** (unbeantwortete Vorab-Frage): ueberspringen und am Ende
   gesammelt melden — kein stiller Verlust
4. **Degradation:** Kein Git-Repo bzw. keine Worktree-Faehigkeit → sequenziell direkt im
   Arbeitsbaum, mit Pflicht-Warnhinweis im Freigabe-Dialog („waehrend des Laufs nicht im
   Repo arbeiten"). Die Lane verweigert nie wegen fehlender Traeger

### Schritt 8: Bericht (`worker-report.md` — Traeger `subagent`; der Pane-Traeger liefert stattdessen den Hand-off-Block)

Jeder SELBST-beendete Worker schreibt VOR seinem Ende den vollen Bericht nach
`features/{slug}/worker-report.md` (status-neutral, zaehlt NICHT fuer die
Statusableitung — Kanon: `DERIVED_STATE_RULES.md` §1.1). Bei harten Stopps
(Task-Verwaltung, Kollisionsregel) bleibt der Diff ohne Report — der koordinierende
Haupt-Agent legt eine Minimal-Notiz an (Ausgang „gestoppt", Zeitpunkt):

```markdown
# Worker-Report: {slug}

**Gestartet:** {YYYY-MM-DD HH:MM} · **Beendet:** {HH:MM} · **Gesamtdauer:** {Min}
**Ausgang:** gruen | Deckel erreicht | teilweise | gestoppt
  (gruen = alle WORKER-ERREICHBAREN Schritte gruen; bei der Freigabe ausgeklammerte
  Schritte weist der Report unter „Was aufgefallen ist" als Abnahme-Aufgaben aus)
**Worktree:** {Pfad} (Diff liegt dort bis zur Abnahme)

## Versuche

| # | Start | Ende | Dauer | Ergebnis |
|---|-------|------|-------|----------|
| 1 | {HH:MM} | {HH:MM} | {Min} | {gruen / rot: woran} |

## Was getan wurde
- {konkrete Aenderungen, je Datei}

## Was verifiziert wurde
- {ausgefuehrte Pruefungen mit Ergebnis — Kommando + Ausgabe-Kern}

## Was aufgefallen ist
- {Nebenbefunde, Ueberraschungen, offene Reste — oder „nichts"}
```

### Schritt 9: Abschluss-Meldung (Traeger `subagent` — der Pane-Traeger meldet ueber die Branch-Verifikation)

Im Chat je Task genau **eine** Sammel-Zeile (Details gehoeren in den Bericht, nicht in
den Chat — Status-Konvention):

```
{slug}: {Ausgang} nach {N} Versuch(en) ({Min} Min) → features/{slug}/worker-report.md
(bis zur Abnahme im Worktree, danach im Haupt-Repo)
{Bei Liste: uebersprungene "teilweise"-Eintraege + gestoppte Worker gesammelt}

Naechster Schritt: Abnahme durch dich — Diff im Worktree pruefen, dann uebernehmen
(Merge/Apply + Commit via /dtb:commit-and-push) oder mit Korrekturhinweis liegen lassen
(zweiter Lauf nutzt den Hinweis als zusaetzliche Vorab-Antwort).
```

Nach Uebernahme ODER endgueltigem Verwerfen: `git worktree remove {Pfad}` (`--force` bei
verworfenem Stand) — keine verwaisten Worktree-Registrierungen zuruecklassen.
