# Derived State — Ableitungsregeln

> **Single Source fuer die Statusableitung.** Alle Lese-Skills (`dtb:workflow-next`,
> `dtb:workflow-status`, `dtb:workflow-resume`, `dtb:backlog-status`) leiten den
> Feature-Status nach DIESEN Regeln aus Artefakten ab. Keine eigene Logik in Skills —
> Aenderungen nur hier.

**Grundprinzip:** Status wird nicht gespeichert, sondern abgeleitet. Quelle der Wahrheit
ist **ein Ordner pro Change** unter `features/<slug>/` mit fixen Dateinamen und die
`## Progress`-Checkboxen in `plan.md` — nicht Statusfelder in BACKLOG.md oder WORKFLOW_STATUS.md.

**Change-Folder-Modell:** Jeder Change ist ein Ordner `features/<slug>/` (Slug in kebab-case,
Regeln in §4) mit festen Dateinamen:

| Datei | Inhalt |
|-------|--------|
| `discovery.md` | Discovery (Anforderungs-Klaerung, optional) |
| `spec.md` | Feature-Spec (Was/Warum) |
| `plan.md` | Implementierungsplan inkl. `## Progress` (Umsetzungsstand) |
| `bug.md` | Bug-Report inkl. `## Fix-Schritte` (statt eigenem Ordner-Change fuer Bugs) |
| `task.md` | Aufgabe inkl. `## Schritte` |
| `review.md` | Impl-Review-Report (`dtb:impl-review`), **status-neutral** — zaehlt NICHT fuer die Ableitung nach §1.1 |
| `fast-draft.md` | Fast-Track-Zwischenspeicher (`dtb:feature-fast`, unbestaetigte Sammelvorlage), **status-neutral** — zaehlt NICHT fuer die Ableitung nach §1.1; ein Ordner NUR mit fast-draft.md gilt als "Idee in Erhebung" (kein ableitbarer Feature-Status) |
| `worker-report.md` | Worker-Bericht (`dtb:worker`, voller Lauf-Report je Task), **status-neutral** — zaehlt NICHT fuer die Ableitung nach §1.1; der Umsetzungsstand einer Aufgabe folgt allein den `## Schritte`-Checkboxen (§1.5) |

Ein archivierter Change ist der ganze Ordner unter `archive/<slug>/`.

---

## 1. Ableitungsregel

### 1.1 Vorhandene Ordner-Dateien → Pipeline-Stage

Pro Change-Ordner `features/<slug>/` gilt die **hoechste** zutreffende Zeile:

| Vorhandene Dateien im Ordner | Abgeleiteter Status |
|------------------------------|---------------------|
| kein Ordner (nur INBOX-Eintrag) | Idee |
| nur `discovery.md` | In Discovery |
| `spec.md` (ohne `plan.md`) | Spezifiziert |
| `plan.md`, 0 Checkboxen abgehakt | Geplant |
| `plan.md`, teilweise abgehakt | In Arbeit |
| `plan.md`, alle Checkboxen abgehakt | Fertig zum Testen |
| Ordner unter `archive/<slug>/` | Abgeschlossen |

### 1.2 Explizite Zustaende (nicht ableitbar)

Diese Zustaende sind bewusste Nutzer-Entscheidungen und ueberschreiben die Ableitung:

- **Pausiert** — manuelle Markierung (WORKFLOW_STATUS "Pausierte Themen" oder BACKLOG-Anmerkung)
- **Abgenommen** — getestet & freigegeben. Einziger Schreiber ist `dtb:workflow-checkpoint`
  (Schritt 2.3, Beleg-Rueckfrage als Verifikations-Gate — nie auf blossen Zuruf). Traegerfeld
  ist die `**Status:**`-Zeile im Kopf von `spec.md` (bei reinen Tasks/Bugs: `task.md`/`bug.md`,
  §1.5). Der Change bleibt unter `features/` (Vorbehalte/Beleg-Luecken bleiben im aktiven
  Bereich sichtbar) und ist damit Archiv-Kandidat (`dtb:archive` Kandidat-Regel)
- **Abgeschlossen** — nur via `/dtb:archive`; die Archivierung IST der Abschluss-Akt.
  100% Checkboxen ≠ automatisch abgeschlossen

**Lese-Regel fuer `Abgenommen` (verbindlich fuer alle Lese-Skills):**

> **Wartungs-Hinweis (Format-Kopplung):** Diese Lese-Regel ist gespiegelt in
> `dtb:workflow-next`, `dtb:backlog-status` und `dtb:workflow-resume` (Autarkie: die
> Regel-Datei ist Klasse-B-Seed und erreicht Bestandsprojekte nicht automatisch).
> `dtb:workflow-status` behandelt explizite Zustaende bereits. Aenderung hier → die drei
> Spiegel mitziehen und mechanisch verifizieren (Grep auf den einzeiligen Kernsatz:
> genau 1 Treffer je Spiegel-Datei, 3 Dateien).

- **Kernsatz (eine Zeile, Grep-Anker der Kopplung):** Ein gesetztes `Abgenommen` ueberschreibt die Ableitung „Fertig zum Testen" und ist KEIN Konflikt nach §1.3 (analog `Pausiert`).
- **Konflikt ist genau eine Kombination:** `**Status:** Abgenommen` gesetzt UND `## Progress`
  unvollstaendig (< Y/Y). Dann gewinnt das Artefakt (der abgeleitete Status) und der
  Widerspruch wird mit 1 Zeile gemeldet:
  `⚠ {Item}: Feld sagt "Abgenommen", ## Progress zeigt "{X/Y}"`.
  Jede andere Kombination ist kein Konflikt.
- **Still-Regel:** Feld fehlt oder traegt den (mit der Ableitung uebereinstimmenden) Wert → still; jeder andere Nicht-`Abgenommen`-Wert faellt unter die normale Konfliktregel §1.3.

### 1.3 Konfliktregel

Widerspricht ein manuelles Statusfeld (z.B. in BACKLOG.md) dem abgeleiteten Zustand:

1. **Das Artefakt gewinnt.** Reports zeigen den abgeleiteten Status.
2. **Der Widerspruch wird gemeldet** (1 Hinweiszeile im Report), nie stillschweigend uebergangen.
3. Lese-Skills korrigieren das Feld NICHT selbst (read-only) — Korrektur erfolgt beim
   naechsten schreibenden Skill (`workflow-checkpoint`) oder manuell.

### 1.4 Fallbacks (Altbestand, defekte Daten)

Kein Fallback fuehrt zum Abbruch — immer definiertes Verhalten:

| Situation | Verhalten |
|-----------|-----------|
| `plan.md` ohne `## Progress`-Sektion | Status "Plan vorhanden, Fortschritt unbekannt"; Nachruestung anbieten |
| `## Progress` mit 0 Checkbox-Zeilen | wie "keine Sektion" |
| Ordner mit `plan.md` ohne `spec.md` | Meldung "Change ohne Spec" (Vollstaendigkeit pruefen) |
| leerer Change-Ordner | ignorieren + Hinweis |
| **flache Alt-Dateien** (`FEATURE_*.md`, `PLAN_*.md` etc. direkt in `features/`) | Altbestand vor Migration; ignorieren fuer Ableitung; Migration anbieten (`/dtb:migrate-change-folders`) |
| **`IMPL_STATUS_*.md`** (Altbestand, abgeschafft) | ignorieren; Migration anbieten |
| gar keine Change-Ordner in `features/` | "Kein aktives Feature" |

### 1.5 Sonderregel `task.md` / `bug.md`

Aufgaben und Bugs haben keinen separaten Plan — ihre Checkliste steht **direkt in der Datei**
(`## Schritte` in `task.md` bzw. `## Fix-Schritte` in `bug.md`). Ableitung analog: 0 abgehakt =
Offen/Analysiert (bug) bzw. Offen (task), teilweise = In Arbeit, alle abgehakt = **Behoben**
(`bug.md`) bzw. **Erledigt** (`task.md`). Es zaehlen ausschliesslich die Checkboxen unter
`## Fix-Schritte`/`## Schritte` — ein separater `## Testplan` in `bug.md` wird NICHT mitgezaehlt.
Explizite Statusfelder im
Kopf dieser Dateien gelten als manuelle Zustaende nach 1.2 nur fuer: Pausiert und Abgenommen
(Schreiber von `Abgenommen` bleibt auch hier `dtb:workflow-checkpoint` Schritt 2.3). Ein Change-Ordner
kann `spec.md`/`plan.md` **und** `bug.md`/`task.md` enthalten (z.B. Bug im Zuge eines Features);
die Ableitung nach 1.1 (plan-basiert) hat dann Vorrang, `bug.md`/`task.md` sind Zusatz-Artefakte.

---

## 2. Progress-Sektion — Format & Verifikations-Gate

Jedes `plan.md` enthaelt eine `## Progress`-Sektion (erzeugt von `dtb:impl-plan`):

```markdown
## Progress

- [ ] 1.1 Kurzname des Schritts
- [x] 1.2 Kurzname des Schritts — `a1b2c3d`
- [x] 1.3 Doku-Schritt ohne Commit
- [x] 2.1 Geflippt, Phase laeuft noch (SHA folgt beim Phasen-Commit)
```

**Regeln:**

1. **Eine Zeile pro Plan-Schritt**, Nummerierung identisch zu den Schritten im Plan (N.M)
2. **Checkbox-Syntax:** `- [ ]` offen, `- [x]` erledigt — keine anderen Marker
3. **Flip-Bedingung (Verifikations-Gate):** Eine Checkbox darf erst geflippt werden, wenn der
   Schritt umgesetzt ist UND kein **Automated**-Checkpoint-Kriterium seiner Phase verletzt ist
   (rotes Kriterium → erst fixen, dann abhaken). Kriterien, die erst spaetere Schritte der
   Phase liefern, gelten als ausstehend, nicht verletzt. Checkpoint-Kriterien einer Phase sind
   unterteilt in **Automated** (mechanisch pruefbar: Kommando, Grep, Datei-Existenz) und
   **Manual** (menschliches Urteil, am Phasen-Ende bestaetigt — Ritual in `dtb:implement`).
   Fehlen Kriterien oder sind sie ungeteilt (Alt-Plan): alle als Manual behandeln —
   das Gate entfaellt nie, es wandert zum Menschen (kein Abbruch, vgl. §1.4)
4. **Commit-SHA als Verifikations-Beleg:** nach ` — ` als Inline-Code (`` `a1b2c3d` ``,
   Kurzform 7 Zeichen). Die SHA wird NICHT beim Abhaken gesetzt, sondern beim
   Phasen-Ende-Commit in alle waehrend der Phase geflippten Zeilen nachgetragen —
   sie belegt damit die verifizierte Phase, nicht nur den Commit. Eine geflippte Zeile
   ohne SHA ist mid-phase ein gueltiger Zwischenzustand. Schritte/Phasen ohne Commit
   (reine Doku/Verifikation, leerer Diff) bleiben dauerhaft SHA-los
5. **Multi-Repo:** Die SHA einer Zeile stammt aus dem Repo des jeweiligen Schritts;
   mehrere SHAs pro Phase sind zulaessig. In Multi-Repo-Projekten (mehr als ein Eintrag
   in `config.repos`) traegt die SHA ein Repo-Praefix im Inline-Code
   (`` `repo-name@a1b2c3d` ``); bei Single-Repo-Projekten bleibt das Format ohne Praefix
6. **Gebuendelte Commits:** ein Commit darf mehrere Checkboxen belegen (gleiche SHA an
   mehreren Zeilen zulaessig)
7. **Kompakt:** max ~30 Zeilen, keine Prosa — Details gehoeren in die Plan-Schritte
8. **Manuelles Abhaken erlaubt:** auch der Mensch darf Checkboxen setzen (Artefakt = Wahrheit);
   die Flip-Bedingung (Regel 3) gilt dabei genauso
9. **Abhaken ist Teil des Implementierungs-Loops:** nach jedem umgesetzten Schritt gemaess
   Flip-Bedingung, nicht gesammelt am Session-Ende; der SHA-Nachtrag erfolgt am Phasen-Ende
   (Regel 4)

---

## 3. Statusmodell — Mapping auf die BACKLOG-Legende

Abgeleitete Zustaende und ihre Anzeige in Reports/BACKLOG:

| Abgeleiteter Status | BACKLOG-Legende | Anzeige-Hinweis |
|---------------------|-----------------|-----------------|
| Idee | Idee | nur INBOX/BACKLOG-Zeile, kein Ordner |
| In Discovery | Idee | Zusatz "(in Discovery)" |
| Spezifiziert | Idee | Zusatz "(Spec erstellt)" — noch kein Plan |
| Geplant | Geplant | Plan existiert, 0% umgesetzt |
| In Arbeit | In Arbeit | Zusatz "X/Y Schritte" aus Checkbox-Zaehlung |
| Fertig zum Testen | Fertig zum Testen | 100% Checkboxen; wartet auf Abnahme |
| Abgenommen | Abgenommen | explizit (1.2) |
| Abgeschlossen | Abgeschlossen | explizit via `/dtb:archive` |
| Pausiert | Pausiert | explizit (1.2), ueberschreibt Ableitung |

**Statusfeld in BACKLOG.md** ist abgeleitete **Anzeige**: schreibende Skills befuellen es
beim naechsten Lauf nach diesen Regeln; manuell gepflegt werden nur Prio und Ziel.

---

## 4. Slug-Ableitung (Change-Ordnername)

Der Ordnername `features/<slug>/` wird aus dem Change-/Feature-Namen abgeleitet.

**Ableitung (deterministisch):**

1. Alles klein schreiben (lowercase)
2. Unterstriche `_` und Leerzeichen → Bindestrich `-`
3. Alle Zeichen ausser `a-z`, `0-9`, `-` entfernen
4. Mehrfache `-` zu einem zusammenfassen; fuehrende/abschliessende `-` strippen

Beispiele: `CHANGE_FOLDER_MODELL` → `change-folder-modell`; `Chat History` → `chat-history`;
`FINN_MIS_AWARENESS` → `finn-mis-awareness`.

**Regeln:**

- **Keine laufenden Nummern** — reine Namens-Slugs (die INBOX-`#` bleibt die ID; der Ordner
  traegt keinen Zahlenpraefix)
- **Kebab-case, stabil:** einmal vergeben bleibt der Slug fix (Umbenennung = bewusster `git mv`)
- **Eindeutigkeit / Kollision:** Leiten zwei verschiedene Change-Namen denselben Slug ab
  (z.B. `FOO_BAR` und `FOO-BAR` → beide `foo-bar`), ist das eine **Kollision**. Schreibende
  Skills und der Migrations-Helfer **brechen ab** und melden die kollidierenden Namen — kein
  automatisches Anhaengen von Suffixen/Nummern. Der Nutzer benennt eine Quelle bewusst um.

---

## 5. Roadmap-Ableitung (ROADMAP.md-Statusspalte)

Die von `dtb:greenfield-roadmap` erzeugte `project-strategy/ROADMAP.md` fuehrt je Slice/Foundation
eine **Change-ID in kebab-case = kuenftiger Feature-Slug** (§4). Die **Status-Spalte** in der
At-a-glance-Tabelle ist eine **abgeleitete Anzeige** („nicht manuell pflegen") — analog §3.

### 5.1 Ableitung (Change-ID → Slug → Ordner-Zustand)

Pro Roadmap-Item gilt die **hoechste** zutreffende Zeile (`<slug>` = Change-ID des Items):

| Zustand im Projekt | Abgeleiteter Roadmap-Status |
|--------------------|-----------------------------|
| Ordner `archive/<slug>/` existiert | `done` |
| Ordner `features/<slug>/` existiert | `in-progress` |
| kein Ordner (Item noch nicht in der Pipeline) | **Doc-Status** gilt: `proposed` / `ready` / `blocked` |

Der **Doc-Status** ist der einzige manuell (vom Roadmap-Autor) gesetzte Wert und gilt nur, solange
kein Change-Ordner existiert. Sobald `feature-discover` einen Ordner anlegt, gewinnt der abgeleitete
`in-progress`; ein archivierter Change wird `done`. Vokabular einheitlich **englisch**
`proposed / ready / blocked / in-progress / done` (Entscheidung F; konsistent zu `S-NN`/`F-NN`).

### 5.2 Konflikt & Sync

- **Konfliktregel §1.3 gilt analog:** Widerspricht die gesetzte Statusspalte dem abgeleiteten
  Zustand, gewinnt das Artefakt (der Ordner-Zustand); lesende Roadmap-Laeufe (Report-Modus) melden
  den Widerspruch mit 1 Hinweiszeile und korrigieren nicht selbst.
- **Sync:** `dtb:workflow-checkpoint` synchronisiert die Spalte beim naechsten Lauf (nur wenn
  `ROADMAP.md` existiert) — dieselbe Mechanik wie die BACKLOG-Spalte, **keine** `dtb:archive`-Kopplung.

---

## 6. Fach-Frage-Konvention (Offene Punkte)

Fragen, die waehrend der Arbeit auftauchen und **nicht sofort/allein beantwortbar** sind
(sie gehoeren ins Fach-Meeting), werden in der Sektion `## Offene Punkte` eines Change-Artefakts
als **statusfaehige, getaggte Checkbox** erfasst — Derived-State-konform, ohne zweiten Speicherort.

### 6.1 Grammatik (dateiunabhaengig)

Eine Fach-Frage ist eine Bullet-Zeile in `## Offene Punkte` der Form:

```markdown
## Offene Punkte

- [ ] [Fach] Wird Export nach SAP zwingend benoetigt?
      → Zwischenstand: Entscheidung vertagt auf Q4 (Meeting 2026-07-20)
- [x] [Fach] Welche Rollen duerfen freigeben?
      → Antwort: nur Teamleiter (Meeting 2026-07-17)
- Report-Layout final klaeren            (untagged = selbst zu klaeren)
```

- **Kanonform:** `- [ ] [Fach] <Frage>` — je ein Leerzeichen zwischen Checkbox, Tag und Frage.
- Die Grammatik gilt **dateiunabhaengig** fuer JEDES `## Offene Punkte` (z.B. `discovery.md`,
  `spec.md`) — nicht an eine bestimmte Datei gebunden.
- **Nur `[Fach]`-Fragen sind statusfaehig** und tragen die Checkbox: `- [ ]` offen,
  `- [x]` beantwortet. Ein normaler offener Punkt ist ein reiner Bullet OHNE Checkbox (siehe §6.3).
- **Nachtrag aus dem Meeting — zwei Fortsetzungsformen** (je eine eingerueckte Zeile unter dem
  Bullet, Eintrag bleibt als Beleg stehen, nicht loeschen):
  - **Vollantwort:** Frage wird abgehakt (`- [ ]` → `- [x]`), Antwort als
    `→ Antwort: … (Meeting YYYY-MM-DD)` **nur unter dem abgehakten Bullet**.
  - **Teilantwort/Zwischenstand:** Frage bleibt **offen** (`- [ ]`), Zwischeninfo als
    `→ Zwischenstand: … (Meeting YYYY-MM-DD)` **nur unter dem offenen Bullet**. Mehrere
    Zwischenstaende ueber die Zeit sind erlaubt (je Meeting einer, **akkumulierend** — Verlauf);
    erst haken, wenn eine echte Antwort vorliegt. Eine spaetere `→ Antwort:` tritt als letzte
    Zeile hinzu, die Zwischenstaende bleiben stehen.
  - Schreibender Konsument beider Formen ist `dtb:meeting-dump` (§6.3).

### 6.2 Status-Neutralitaet (Abgrenzung zu §1/§2)

Fach-Frage-Checkboxen in `## Offene Punkte` sind **status-neutral** — sie zaehlen NICHT fuer
die Feature-Statusableitung (§1) und nicht fuer das Verifikations-Gate (§2). Nur `## Progress`
(bzw. `## Schritte`/`## Fix-Schritte`, §1.5) speisen die Ableitung. Damit verhaelt sich die
Sektion analog zu `review.md` (status-neutrale Ordner-Datei). Der `dtb:implement`-Loop und alle
Lese-Skills bleiben **blind** gegen `## Offene Punkte`-Checkboxen.

### 6.4 Becken-Eintraege (`INBOX-BEFUNDE.md`) sind status-neutral

Ein Eintrag im Befund-Becken ist **kein Vorgang** und **keine Idee** im Sinne der Ableitung:
die Tabelle in §1 („kein Ordner, nur INBOX-Eintrag → Idee") gilt allein fuer `INBOX.md`. Ein
Becken-Eintrag zaehlt nirgends — nicht fuer die Feature-Statusableitung (§1), nicht fuer das
Verifikations-Gate (§2), nicht fuer Arbeits-Ansichten. Er wird zum Vorgang erst durch die
**Befoerderung** nach `INBOX.md` (`dtb:idea-triage`), und dort ist er dann eine normale Idee
mit Status `Offen`. Die Sichtung-Spalte (leer / `L1 YYYY-MM-DD` / `Altbestand`) ist ein
Arbeitsvermerk der Triage, kein Status. Verhaelt sich damit analog zu den Fach-Fragen (§6.2)
und zu `review.md` — sichtbar, aber ableitungsblind.

### 6.3 Rueckwaertskompatibilitaet & Abgrenzung

- Ein Bullet **ohne** `[Fach]`-Tag ist ein normaler „selbst-zu-klaeren"-Punkt (reiner Bullet
  OHNE Checkbox) und bleibt unveraendert gueltig — keine Migration bestehender `## Offene Punkte` noetig.
- **Zwei Renderings, drei Intents:** getaggt `- [ ] [Fach] …` (Fall c: gehoert ins Fach-Meeting,
  nicht sofort/allein beantwortbar) vs. untagged Bullet (Faelle a+b, syntaktisch identisch:
  (a) normaler offener Punkt / (b) „nie erfinden"-Luecke). Nur (c) traegt Tag und Checkbox.
- Die Ableitung Fach-Frage `[ ]`=offen / `[x]`=beantwortet hat zwei Konsumenten: **lesend**
  die Agenda-Ansicht `dtb:meeting-agenda` (#25), die vor dem Meeting alle offenen Fragen aus
  `features/*/{discovery,spec}.md` einsammelt; **schreibend** der
  Meeting-Rueckfluss `dtb:meeting-dump` (#24), der nach einem Meeting Vollantworten (`[x]` +
  `→ Antwort:`) bzw. Zwischenstaende (`[ ]` + `→ Zwischenstand:`, §6.1) nachtraegt — er kippt
  nur die Checkbox und haengt die Fortsetzungszeile an, status-neutral (§6.2), legt aber nie
  neue `[Fach]`-Fragen an (das tut `dtb:open-question`).
- *Ausblick (nicht Teil der Konvention):* eine zweite Tag-Variante ist denkbar, aber bewusst
  noch nicht spezifiziert.

---

## 7. Plan-Kopf-Statusfeld (Review-Nachweis)

Das `plan.md` traegt im Kopf ein `**Status:**`-Feld. Es ist **kein** Umsetzungs-Status (den
liefert ausschliesslich `## Progress`, §2), sondern ein **reiner Review-Nachweis**: Es sagt aus,
ob der Plan ein `dtb:plan-review` bestanden hat und damit startklar ist.

### 7.1 Definitionsfenster, Wertemenge & Vermerkform

- **Definitionsfenster (verbindlich):** Das Kopf-Statusfeld IST die `**Status:**`-Zeile
  **innerhalb der ersten 10 Zeilen** von `plan.md`. Eine `**Status:**`-Zeile ausserhalb dieses
  Fensters ist KEIN Kopf-Statusfeld — sie wird weder gelesen noch von einem Pfleger angefasst
  (schuetzt zitierte Bloecke und Template-Beispiele im Fliesstext vor Fehlgriffen).
- **Wertemenge:** genau zwei Werte — `Entwurf` (kein bestandenes Review) und `Reviewed`
  (Review bestanden, Plan startklar). Die frueheren Werte `In Umsetzung`/`Abgeschlossen` sind
  **abgeschafft** (der Umsetzungsstand kommt aus `## Progress`); zur Lese-Toleranz siehe 7.3.
- **Vermerkform:** `{Wert} ({Urheber} {YYYY-MM-DD}: {Kurzbegruendung})` — das erste Wort in der
  Klammer nennt den **Urheber**, z.B. `Reviewed (plan-review 2026-07-19: REVISE → 3 WARNs behoben)`
  oder `Entwurf (plan-review 2026-07-30: RETHINK)`.
- **Parse-Regel (verbindlich):** Gelesen wird ausschliesslich das **erste Wort** nach
  `**Status:**`. Alles danach ist **Annotation** und wird ignoriert — sowohl der Klammer-Vermerk
  als auch ein HTML-Kommentar (`<!-- … -->`, so erzeugt vom `dtb:impl-plan`-Template). Eine
  Annotation macht den Wert nie zu einem „unbekannten Wert" nach §7.3; unbekannt ist nur ein
  **erstes Wort**, das in keiner Zeile der Matrix in §7.3 vorkommt.

### 7.2 Pfleger & Wertematrix (genau ein Schreiber)

Pfleger des Felds ist **ausschliesslich `dtb:plan-review`**. Es schreibt bei JEDEM Verdikt —
auch bei negativem —, damit das Feld immer den letzten Review-Stand dokumentiert und nie
stillschweigend veraltet. Fehlt die Feld-Zeile, wird sie an der Kopfposition eingefuegt.

| Review-Ausgang | Feld danach |
|----------------|-------------|
| SOUND | `Reviewed (plan-review {YYYY-MM-DD}: SOUND)` |
| REVISE, Findings im selben Zug behoben | `Reviewed (plan-review {YYYY-MM-DD}: REVISE → {N} WARNs behoben)` |
| REVISE, Findings offen | `Entwurf (plan-review {YYYY-MM-DD}: REVISE — Findings offen)` |
| RETHINK | `Entwurf (plan-review {YYYY-MM-DD}: RETHINK)` |

**Harte „behoben"-Bedingung (binaer, kein Ermessen):** `Reviewed` nur, wenn ALLE
WARN-getriebenen Anpassungen tatsaechlich in `plan.md` geschrieben wurden; Teilannahme,
Vertagung oder Ablehnung ergeben `Entwurf (… Findings offen)`. Grund (asymmetrisches Risiko):
`Reviewed` schaltet in `dtb:workflow-next` „Start ausstehend" frei — ein zu frueh gesetztes
`Reviewed` schickt jemanden mit bekannten, unbehobenen Schwaechen in die Umsetzung.

> **Wartungs-Hinweis (Format-Kopplung):** Diese Wertematrix ist woertlich gespiegelt in
> `dtb:plan-review` Schritt 6.1 (der Skill muss autark funktionieren — die Regel-Datei ist
> Klasse-B-Seed und erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22). Aenderst du
> die Matrix hier, ziehe sie dort mit; der Gegen-Hinweis steht im Skill.

**Kein zweiter Schreiber:** `dtb:workflow-checkpoint` synchronisiert dieses Feld ausdruecklich
NICHT (seine Sync-Ziele bleiben BACKLOG-Spalte, `spec.md`/`task.md`, ggf. ROADMAP nach §5) —
zwei Schreiber mit unterschiedlicher Logik waeren die naechste Drift-Quelle.

**Manueller Flip = dokumentierte Ausnahme:** Der Mensch darf das Feld setzen (Artefakt =
Wahrheit, analog §2 Regel 8), dann aber mit Urheber-Vermerk:
`Reviewed (manuell {YYYY-MM-DD}: {Grund})`. Ein manueller Flip gibt sich nie als Review-Ergebnis aus.
Normalweg nach spaeter eingearbeiteten Findings bleibt ein erneuter `plan-review`-Lauf — nur er
prueft, ob die Einarbeitung die WARNs wirklich behebt.

### 7.3 Lese-Regeln (Toleranz & Konfliktmeldung)

Lesende Skills (`dtb:workflow-next`, `dtb:workflow-status`) wenden diese Matrix an:

> **Wartungs-Hinweis (Format-Kopplung):** Diese Toleranz-Matrix ist gespiegelt in
> `dtb:workflow-next` (Quellen-Abschnitt) und `dtb:workflow-status` (Ableitungs-Abschnitt) —
> aus demselben Autarkie-Grund wie in §7.2. Aenderung hier → beide Skills mitziehen.
> `dtb:backlog-status` liest das Feld bewusst NICHT mehr (§7.4 status-neutral) und braucht
> keine Kopie.

| Gelesener Zustand | Behandlung |
|-------------------|------------|
| `Reviewed` | Review bestanden |
| `Entwurf` | Review ausstehend |
| Feld fehlt / liegt ausserhalb des Fensters (7.1) | wie `Entwurf`, **still** (fehlende Information ist kein Konflikt) |
| Altwerte `In Umsetzung` / `Abgeschlossen` | wie `Reviewed`, **still** (setzen logisch ein bestandenes Review voraus) |
| unbekannter Wert (Tippfehler/Freitext) | wie fehlend + **1 Hinweiszeile** „unbekannter Statuswert {X}" |

- **Guard-Pflicht:** Ein Vorschlag „Review ausstehend" darf nur bei **0/Y** abgehakten
  `## Progress`-Checkboxen ausgegeben werden. Bei teilweise oder vollstaendig abgehaktem
  Progress ist ein plan-review-Vorschlag falsch — dort gelten die Ableitungen nach §1.1.
- **Konfliktmeldung (§1.3 analog):** **Konflikt ist genau eine Kombination:** ein physisch
  vorhandenes Feld, das als `Entwurf` gilt, UND ≥1 abgehakte `## Progress`-Checkbox. Jede andere
  Kombination ist **kein** Konflikt — insbesondere `Reviewed` oder ein tolerierter Altwert bei
  beliebigem Progress, denn das Feld sagt nichts ueber den Umsetzungsstand (§7.4).
  Im Konfliktfall gewinnt das Artefakt und der Widerspruch wird mit 1 Zeile gemeldet, nicht
  selbst korrigiert (read-only):
  `⚠ plan.md-Kopf sagt "{Wert}", ## Progress zeigt "{X/Y}"`.
  **Vorrang der Still-Regel:** Die Konfliktmeldung gilt nur fuer ein **physisch vorhandenes**
  Feld mit bekanntem Wert. Als `Entwurf` behandelte Leerstellen (Feld fehlt oder liegt ausserhalb
  des Fensters) bleiben still — auch bei teilweise abgehaktem Progress. Sonst wuerde der
  haeufigste Altbestand (Plan ohne Feld, laufende Umsetzung) dauerhaft eine ⚠-Zeile erzeugen,
  obwohl gar keine widerspruechliche Aussage existiert.
- **Selbstheilung statt Migration:** Altwerte und fehlende Felder werden beim naechsten
  `plan-review`-Lauf normalisiert (7.2 schreibt immer) — eine Bestandsmigration ist nicht noetig.

### 7.4 Status-Neutralitaet (Abgrenzung zu §1/§2)

Das Kopf-Statusfeld ist **status-neutral** — es speist weder die Feature-Statusableitung (§1)
noch das Verifikations-Gate (§2). Es beantwortet ausschliesslich die Frage „hat dieser Plan ein
Review bestanden?" und dient damit dem Pipeline-Gate „Plan-Review" in den Uebersichts-Skills.
Der `dtb:implement`-Loop bleibt gegen dieses Feld blind.

---

## 8. INBOX-Status `Ausgearbeitet` — Change-Link-Pflicht

`Ausgearbeitet` heisst „Change angelegt". Die Aussage gilt nur mit Beleg — sonst faellt eine
Idee, deren Change nie entstanden ist, aus allen Sichten und wird archivierbar (INBOX #95 (1)).

> **Wartungs-Hinweis (Format-Kopplung):** Kernsatz und Verhaltens-Tabelle sind gespiegelt in
> `dtb:archive`, `dtb:project-health`, `dtb:workflow-next`, `dtb:workflow-status` und
> `dtb:idea-rank` (Kopie ist Absicht — Seed erreicht Bestandsprojekte nicht automatisch,
> INBOX #22). Aenderung hier → die fuenf Spiegel mitziehen (Grep-Anker: `Change fehlt`).

### 8.1 Gueltiger Change-Link

Eine INBOX-Zeile mit Status `Ausgearbeitet` ist **belegt**, wenn sie mindestens einen dieser Links
traegt und das Ziel existiert:

- `→ features/{slug}/spec.md`, `→ features/{slug}/task.md` oder `→ features/{slug}/bug.md` — die
  verlinkte Datei existiert
- `→ archive/{slug}/…` — der Ordner `archive/{slug}/` existiert (Change abgeschlossen)

Ein Link nur auf `discovery.md` belegt NICHT (Discovery laeuft = `In Arbeit`, §1.1) — die Diagnose
`dtb:project-health` haengt dann den Hinweis `(nur Discovery verlinkt — Status waere In Arbeit)` an
(die Anzeige-Sichten nicht: fuer sie genuegt der naechste Schritt `/dtb:feature-plan {slug}`).
Links stehen in der Spalte „Idee", Pfade relativ zu `{config.paths.workflows}`; mindestens ein gueltiger Link genuegt (ein zusaetzlicher toter Link macht die Zeile nicht ungueltig); ein toter `features/{slug}/`-Link gilt als belegt, wenn `archive/{slug}/` existiert (Change inzwischen archiviert).

### 8.2 Anzeige-Zustand „Ausgearbeitet, Change fehlt"

- **Kernsatz (eine Zeile, Grep-Anker der Kopplung):** `Ausgearbeitet` ohne gueltigen Change-Link (8.1) ist „Ausgearbeitet, Change fehlt" und zaehlt als offen.
- **Kein neuer Statuswert:** Das Feld bleibt `Ausgearbeitet`; „Change fehlt" ist ein abgeleiteter
  Anzeige-Zustand. Lese-Skills korrigieren nichts (§1.3). Geheilt wird er, sobald der Change
  entsteht: `dtb:task` Schritt 4b bzw. `dtb:feature-plan` Schritt 9 haengen den Link an.
- **Naechster Schritt (deterministisch, eine Zeile, Grep-Anker):**
  Naechster Schritt bei „Change fehlt" (erster zutreffender Zweig gilt): Vermerk „als Aufgabe geroutet" → `/dtb:task {N}`; Link auf `features/{slug}/` mit vorhandener `discovery.md` → `/dtb:feature-plan {slug}`; sonst → `/dtb:feature-discover {N}`.
- **Task-Lane:** `dtb:idea-review` setzt bei der Task-Lane weiterhin `Ausgearbeitet` (Entscheidung
  impl-review F2, 2026-08-02 — kein `In Arbeit`), mit Vermerk
  `→ als Aufgabe geroutet ({Datum}); task.md ausstehend — /dtb:task {N}`. Genau dieser
  Zwischenzustand ist „Change fehlt", bis `dtb:task` laeuft.
- **Teil-Routing** (Lektion L19) bleibt unberuehrt: eine teilweise geroutete Idee steht auf `Offen`.

| Konsument | Verhalten bei „Change fehlt" |
|-----------|------------------------------|
| `dtb:archive` | kein Archiv-Kandidat; eigener Meldeblock „Nicht archiviert — Change fehlt: #{N} → {naechster Schritt}" |
| `dtb:project-health` | WARNUNG „#{N} Ausgearbeitet, Change fehlt" (Report-Zeile ⚠, nicht ❌); zaehlt NICHT als archivierbar |
| `dtb:workflow-next` | Pipeline-Zeile „INBOX `Ausgearbeitet`, Change fehlt" → naechster Schritt — nur wenn zum verlinkten Slug KEIN Change-Ordner existiert (sonst traegt der Ordner-Eintrag den Hinweis); ans Ende sortiert |
| `dtb:workflow-status` | zaehlt pipeline-relevant (Queue-Zeile „Inbox (Change fehlt)"); mit Change-Ordner zum Slug NICHT separat gezaehlt |
| `dtb:idea-rank` | EINE Hinweiszeile unter der Tabelle „offen, Change fehlt: #{N}" — die Tabelle selbst bleibt bei `Offen`; als Vorbedingung: nicht erfuellt |

---

## 9. Lebenslauf offener Aufgaben (WORKFLOW_STATUS `## Offene Aufgaben`)

Eine offene Aufgabe verschwindet nie ohne Spur und weiss, seit wann sie offen ist
(INBOX #95 (2)+(3)). Beides ist EIN Mechanismus: der Vergleich im Checkpoint.

> **Wartungs-Hinweis (Format-Kopplung):** Kernsatz, Zeilenformat, Abgangsvermerke und die
> ⏳-Regel sind kompakt gespiegelt in `dtb:workflow-checkpoint` (Kopie ist Absicht — Seed
> erreicht Bestandsprojekte nicht automatisch, INBOX #22). Aenderung hier → dort mitziehen
> (Grep-Anker: `Aufgaben-Abgaenge`).

### 9.1 Fuehrende Liste & Zeilenformat

- **Fuehrend** ist `## Offene Aufgaben` in `WORKFLOW_STATUS.md` — die Liste, die von Checkpoint zu
  Checkpoint weitergetragen wird. `### Naechste Schritte` im Session-Log ist eine Momentaufnahme
  und uebernimmt die Punkte samt `(seit …)` — ohne Kontext, `· behalten` und ⏳.
- **Zeilenformat:** `- [ ] {Aufgabe} — Kontext: {kurz} (seit YYYY-MM-DD[ · behalten YYYY-MM-DD])`
- **`seit`** wird beim Uebertrag **woertlich** mitgenommen, nie neu gesetzt. Neue Punkte bekommen
  das heutige Datum.
- Die Checkboxen dieser Liste sind **status-neutral** (analog §6.2): sie speisen keine Ableitung.
- **Vorrang vor der Zeilengrenze** von `WORKFLOW_STATUS.md` (60-80 Zeilen): die Liste wird nie still gekuerzt;
  sie schrumpft nur ueber Abgangsvermerke (9.3), Ueberlauf baut die ⏳-Vorlage (9.4) ab.

### 9.2 Vergleich (vor dem Log-Schreiben)

- **Kernsatz (eine Zeile, Grep-Anker der Kopplung):** Jeder Punkt der bisherigen Liste wird entweder weitergetragen oder bekommt genau einen Abgangsvermerk in `### Aufgaben-Abgaenge` — kein Punkt verschwindet ohne Spur.
- **Zeitpunkt:** beim Informationen-Sammeln, VOR dem Schreiben des Session-Logs (der Log braucht
  die Abgaenge bereits).
- **Basis:** die `WORKFLOW_STATUS.md` auf der Platte, gelesen VOR dem Ueberschreiben — kein Git
  noetig. Fehlt die Datei oder die Sektion → kein Vergleich, alle Punkte gelten als neu.
- **Zuordnung** nach Sinn, nicht nach Wortlaut: ein umformulierter Punkt ist derselbe Punkt, sein
  `seit` wandert mit. Ist die Zuordnung unsicher → Rueckfrage („ist X = Y?"), nie raten. Naechste
  Schritte aus dem Chat, die keinem alten Punkt entsprechen, sind neue Punkte (`seit` = heute).

### 9.3 Abgangsvermerke (`### Aufgaben-Abgaenge` im Session-Log)

Einfache Aufzaehlung, **KEINE Checkboxen** (nichts, das eine Ableitung mitzaehlen koennte —
Muster WORKTREE-HANDOFF-Block). Der Abschnitt entfaellt bei 0 Abgaengen.

```markdown
### Aufgaben-Abgaenge
- erledigt: {Aufgabe} (seit YYYY-MM-DD)
- verworfen: {Aufgabe} (seit YYYY-MM-DD) — Grund: {Grund}
- aufgegangen in „{Ziel}": {Aufgabe} (seit YYYY-MM-DD)
```

- **`verworfen` ohne Grund ist unzulaessig** (Muster `archive/INBOX-BEFUNDE-verworfen.md`).
- **Welcher Vermerk:** belegt die Session die Erledigung → `erledigt`; deutet sie einen Abgang ohne
  Beleg an → Rueckfrage; ohne Session-Signal wird der Punkt still weitergetragen — nie still gestrichen.
- **Zusammengelegt/aufgeteilt/ersetzt** (ersetzt = 1:1 durch einen Nachfolger, NUR wenn die Session die Abloesung
  ausdruecklich nennt; sonst alter Punkt `erledigt`/weiter + neuer Punkt `seit` heute, unsicher → Rueckfrage): Vermerk
  `aufgegangen in …` (Vorrang vor „neuer Punkt" aus 9.2); der Ziel-Punkt erbt das **aelteste** `seit` der beteiligten Punkte — sonst liesse
  sich das Alter durch Umformulieren zuruecksetzen.

### 9.4 Alter & ⏳

- **Schwelle:** `status.alter_schwelle_tage` in `workflow.config.yaml`, **Default 7** bei fehlendem Key.
- **Faellig:** heute − (juengeres Datum von `seit` und `behalten`) ≥ Schwelle → Punkt wird mit ⏳
  am Zeilenende markiert (nach `(seit …)`). Geprueft wird die **neue** Liste, nach den Zuordnungs-Rueckfragen aus 9.2
  (deren Antwort bestimmt `seit`).
- **EINE Sammelvorlage** fuer alle faelligen Punkte (nie N Einzelfragen), Default „behalten":

```
⏳ {K} offene Aufgabe(n) liegen ≥ {S} Tage:
  1. {Aufgabe} (seit YYYY-MM-DD, {T} Tage)
  …
„passt" = alle behalten · je Zeile: „{Nr} erledigt" | „{Nr} verwerfen: {Grund}" · „Abbruch"
```

- **„behalten"** haengt `· behalten YYYY-MM-DD` an (`seit` bleibt, ⏳ entfaellt) → naechste Frage erst
  nach der naechsten Schwelle. **Abbruch** → keine Entscheidung, die Punkte bleiben mit ⏳, die Frage
  kommt beim naechsten Mal. **Andere Antwort** → genau eine Rueckfrage
  (`passt / {Nr} erledigt / {Nr} verwerfen: {Grund} / Abbruch?`), bleibt sie unklar → Abbruch.
- Erledigen/Verwerfen erzeugt den Abgangsvermerk nach 9.3. Keine automatische Entscheidung.

### 9.5 Sonderfaelle

| Situation | Verhalten |
|-----------|-----------|
| erster Checkpoint nach Einfuehrung (Punkte ohne `seit`) | Datum aus dem ersten Auftreten im Session-Log rekonstruieren, Form `(seit ≤YYYY-MM-DD)`; nichts gefunden → heutiges Datum mit `≤` |
| Punkte aus einem WORKTREE-HANDOFF | `seit` = Datum aus der Hand-off-Kopfzeile |
| Checkpoint im verlinkten Worktree | kein Vergleich (Voll-Guard bricht ab); holt der naechste Orchestrator-Checkpoint nach |
| leere Liste | kein Vergleich, kein Vermerk |
| Altbestand (alte `WORKFLOW_STATUS`-Versionen, alte Logs) | keine rueckwirkende Aufarbeitung |

---

## 10. Worktree-Stand (Arbeit ausserhalb des Haupt-Checkouts)

Arbeit in verlinkten Worktrees (`dtb:pane-start`, `dtb:worker`) ist bis zum Merge fuer die
Lese-Sichten unsichtbar, und erledigte Worktrees leben weiter (INBOX #95 (4) + Aufraeum-Luecke).
Diese Regel macht beides beim Aufruf sichtbar — rein lesend, ohne Ueberwachung (#97).

> **Wartungs-Hinweis (Format-Kopplung):** Kernsatz, Zeilenformat und Zustands-Tabelle sind
> gespiegelt in `dtb:workflow-resume`, `dtb:workflow-next` und `dtb:backlog-status` (Kopie ist
> Absicht — Seed erreicht Bestandsprojekte nicht automatisch, INBOX #22). Aenderung hier → die
> drei Spiegel mitziehen (Grep-Anker: `In Worktrees`). **Vierter Spiegel (nur Stand-Felder
> aus 10.2):** `dtb:worker` → `#### Rueckweg: Ueberwachungs-Tick` (Signal 2 der Pruefliste —
> Commits, uncommitted, Fortschritt; eigener Grep-Anker ist der Sektionstitel, da der Tick
> keinen `In Worktrees`-Block ausgibt).

### 10.1 Quelle & Umfang

- **Kernsatz (eine Zeile, Grep-Anker der Kopplung):** Die Sichten zeigen unter `In Worktrees` je verlinktem Worktree genau eine Zeile — gelesen, nie beschrieben.
- **Quelle:** `git worktree list --porcelain`. Der **erste** Eintrag ist der Haupt-Checkout und
  wird nicht gelistet; die Zeilen folgen der Reihenfolge der Liste.
- **Block entfaellt still**, wenn das Projekt kein Git-Repo ist (`git rev-parse --git-dir` scheitert) oder es
  keinen weiteren Worktree gibt (kein „keine"-Rauschen). Scheitert `git worktree list` dagegen IM Git-Repo →
  genau eine Zeile `In Worktrees: nicht lesbar ({Fehler})` — ein geschluckter Fehler wuerde alle Worktree-Arbeit verbergen.
- **Slug:** Verzeichnisname ohne Praefix `pane-`/`worker-`; sonst der Verzeichnisname.
- **Art:** Praefix `pane-` → `interaktiv (pane)`; `worker-` mit Branch → `autonom (pane)`;
  `worker-` ohne Branch (detached) → `autonom (subagent)`; alles andere (von Hand, Harness) → `manuell`.

### 10.2 Zeilenformat

```
In Worktrees:
  {slug}  {Art}  {branch | detached}  {Stand}  {N} uncommitted  {Fortschritt}[  ⏳]
```

- **Stand:** `+{n} Commits, zuletzt YYYY-MM-DD` (n = Commits des Branches, die nicht im Hauptbranch
  sind; Datum des letzten Commits) — oder ein Zustand aus 10.3.
- **uncommitted:** Zahl der Eintraege aus `git -C {pfad} status --porcelain`.
- **Fortschritt** wird aus dem **Worktree-Pfad** gelesen (aktueller Stand inkl. uncommitteter
  Flips), in dieser Reihenfolge: `{pfad}/{config.paths.workflows}/features/{slug}/plan.md` →
  `## Progress` → `Progress X/Y` · sonst `task.md` → `## Schritte` → `Schritte X/Y` · sonst Stage-Name nach §1.1 (z.B.
  `Discovery`, `Spezifiziert`) · sonst `—`.
- **Detached HEAD** (kein Branch, z.B. Subagent-Worker): Branch-Feld zeigt `detached @{sha7}`, das
  Feld „Stand" entfaellt (ohne Branch keine Historie — weder `frisch` noch `gemergt`); statt
  Fortschritt `worker-report {vorhanden | fehlt}` (Datei im Worktree-Pfad des Change-Ordners).

### 10.3 Zustaende (Vorrang von oben nach unten)

| Zustand | Erkennung | Anzeige im Feld „Stand" |
|---------|-----------|-------------------------|
| verwaist | Eintrag traegt `prunable` bzw. Pfad fehlt | `verwaist → git worktree prune` (Rest der Zeile entfaellt) |
| laufend | n > 0 (Commits des Branches, die nicht im Hauptbranch sind) | `+{n} Commits, zuletzt YYYY-MM-DD` |
| gemergt | n = 0 UND Branch hatte eigene Commits (Branch-Reflog hat mehr als den Anlage-Eintrag) | `gemergt → aufraeumen (git worktree remove "{pfad}")`; bei uncommitted > 0 stattdessen `gemergt, {N} uncommitted → erst sichern` — nie zum Entfernen raten, solange Arbeit ungesichert ist (Rest der Zeile entfaellt in beiden Faellen) |
| frisch | alles andere (n = 0, Reflog nur mit Anlage-Eintrag oder fehlend) | `frisch` — nie „aufraeumen" |

- **Warum der Reflog:** Ein frisch angelegter Branch und ein gemergter Branch haben beide 0 Commits
  gegenueber dem Hauptbranch; nur die Branch-Historie unterscheidet sie. Fehlt der Reflog (z.B.
  deaktiviert) → im Zweifel `frisch` (nie faelschlich „aufraeumen").
- **Grenze Squash-/Rebase-Merge:** die Commits des Branches erscheinen nicht im Hauptbranch → n > 0, der
  Worktree bleibt `laufend` (auch mit ⏳). Ob er erledigt ist, entscheidet der Mensch — nie als offene Arbeit werten.
- **⏳** haengt an `frisch`/`laufend`, wenn der letzte Commit (bei `frisch`: die Anlage) ≥
  `status.alter_schwelle_tage` Tage alt ist (gleicher Vergleich wie §9.4, Default 7).
- „aufraeumen" und „prune" sind **Hinweise**; abbauen tut der Mensch bzw. der zustaendige Skill.

### 10.4 Hauptbranch & Lese-Grenze

- **Hauptbranch:** `parallel.default_branch` aus `workflow.config.yaml`, falls gesetzt; sonst der
  Branch des ersten `git worktree list`-Eintrags (Haupt-Checkout). Kein Raten zwischen master/main.
- **Erlaubt (nur lesend):** `git worktree list --porcelain`, `git rev-list --count`, `git log -1`,
  `git reflog show`, `git rev-parse --git-dir`, `git -C {pfad} status --porcelain`, Dateien unter `{pfad}` lesen.
- **Nie:** `checkout`, `add`, `commit`, `stash`, `worktree remove`/`prune` ausfuehren oder
  Dateien im Worktree schreiben — Schreibgrenzen-Regel (`skills/CLAUDE.md` → „Parallele Sessions")
  und Worktree-Guard bleiben unveraendert.

---

**Eingefuehrt mit:** Feature DERIVED_STATE (`features/FEATURE_DERIVED_STATE.md`), 2026-07-06
**Umgestellt auf Change-Folder-Modell:** Feature CHANGE_FOLDER_MODELL, 2026-07-09
**§5 Roadmap-Ableitung ergaenzt:** Feature greenfield-autoren-skills, 2026-07-13
**§2 gehaertet (Verifikations-Gate: Flip-Bedingung, SHA-Timing, Multi-Repo-SHA):** Feature verifikations-gate, 2026-07-15
**`review.md` als status-neutrale Ordner-Datei ergaenzt:** Feature impl-review, 2026-07-16
(Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22)
**§6 Fach-Frage-Konvention ergaenzt:** Feature fachfragen-erfassung, 2026-07-17
(Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22)
**§6.1 `→ Zwischenstand:`-Form + §6.3 schreibender Konsument ergaenzt:** Feature meeting-dump, 2026-07-21
(Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22)
**§7 Plan-Kopf-Statusfeld (Review-Nachweis) ergaenzt:** Feature plan-status-feld, 2026-07-30
(Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22)
**`fast-draft.md` als status-neutrale Ordner-Datei ergaenzt:** Feature feature-fast, 2026-08-02
(Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22)
**§6.3 lesender Konsument benannt (`dtb:meeting-agenda` statt „#25, noch offen"):** Feature
meeting-agenda, 2026-08-02 (Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch,
vgl. INBOX #22 — **sechster** dokumentierter Skew-Fall)
**`worker-report.md` als status-neutrale Ordner-Datei ergaenzt:** Feature autonome-schiene,
2026-08-08 (Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22 —
**siebter** dokumentierter Skew-Fall)
**§8 Change-Link-Pflicht, §9 Lebenslauf offener Aufgaben, §10 Worktree-Stand ergaenzt:** Feature
statusverlust-luecken, 2026-09-23 (Seed-Aenderung — die Konsumenten tragen operative Kopien,
vgl. INBOX #22)
