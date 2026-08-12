---
name: dtb:feature-fast
description: >-
  Use when: "fast track", "feature fast", "kleines Feature schnell",
  "Schnelldurchgang", "Fast-Track". Fast-track lane for small features:
  bundles the discover/spec/plan interviews into ONE pass with reasoned
  default assumptions (max. 3 core questions) and one vetoable summary
  template; writes discovery.md, spec.md and plan.md only after user
  approval — derived state, gates and reviews stay unchanged.
disable-model-invocation: true
argument-hint: "[INBOX-Nummer oder Stichwort]"
allowed-tools: Read, Write, Glob, Grep, Bash
pipeline:
  stage: planning
  after: [dtb:idea-review, dtb:feature-discover]
  next: [dtb:plan-review]
  consumes: [INBOX.md, workflow.config.yaml, features/*/discovery.md, features/*/spec.md, features/*/plan.md, project-rules/lessons.md]
  produces: [features/*/discovery.md, features/*/spec.md, features/*/plan.md, features/*/fast-draft.md, INBOX.md, BACKLOG.md]
---

# Fast-Track: kleines Feature in einem Durchgang

Du buendelst fuer ein KLEINES Feature die Erhebung der drei Stationen `feature-discover`,
`feature-plan` und `impl-plan` zu einem Durchgang: Du befuellst alle Template-Abschnitte mit
begruendeten Default-Annahmen, stellst hoechstens 3 Kernfragen und legst EINE vetobare
Sammelvorlage vor. Erst nach dem Ok des Nutzers schreibst du `discovery.md`, `spec.md` und
`plan.md` — vollstaendig konventionskonform, sodass die nachgelagerte Kette (plan-review,
implement, impl-review) und die Statusableitung nichts vom Fast-Track merken.

Du VERKUERZT die Erhebung, nie die Absicherung: Derived State, Hard-Gates und beide Reviews
gelten unveraendert.

## Schritt 0: Config laden

Lies `workflow.config.yaml` im Projekt-Root.

Falls nicht vorhanden: Verwende Fallback-Pfad `dtb-project/project-workflows/`.

## Lektionen als Prior lesen

Lies `{config.paths.rules}/lessons.md` (Fallback: `dtb-project/project-rules/lessons.md`).

- Fehlt die Datei oder ist sie leer (keine Datenzeile unter der `|---|`-Trennzeile) →
  diesen Schritt still ueberspringen (kein Abbruch)
- Sonst: filtere Eintraege, deren `Applies-to` `feature-fast`, `impl-plan` (der Fast-Track
  ersetzt dessen Planerstellung) oder `alle` enthaelt
- Wende die passenden `Rule`-Aussagen bei Erhebung und Artefakt-Erzeugung still an
- Gib **einen** kompakten Hinweis aus: `📚 {N} Lektion(en) beruecksichtigt`
- **Konflikt** (zwei behaltene Lektionen mit gegensaetzlicher `Rule`): beide zeigen und
  den Widerspruch melden — nicht selbst aufloesen

---

## Schritt 1: Eingangs-Gate (INBOX-Pflicht) + Bestandsaufnahme

1. **Idee laden** aus `{config.paths.workflows}/INBOX.md`:
   - Argument uebergeben → nach Nummer oder Stichwort suchen
   - Kein Argument → Eintraege mit Status `In Arbeit` filtern; genau einer → nehmen,
     mehrere → Auswahl anbieten, keiner → Gate greift (unten)
2. **Gate — kein passender INBOX-Eintrag:**

   ```
   ⛔ feature-fast braucht einen INBOX-Eintrag (Pflicht-Vorstufe, kein Ad-hoc-Einstieg).
      Geprueft: {config.paths.workflows}/INBOX.md — kein Eintrag "In Arbeit" bzw. kein
      Treffer fuer "{Argument}".
      → Idee zuerst erfassen: /dtb:idea {Beschreibung}
      → oder Idee im Review auswaehlen: /dtb:idea-review
   ```

   Hier stoppen — die INBOX ist die einzige Erhebungsquelle des Fast-Track.
3. **Slug ableiten** (kebab-case, Regeln: `{config.paths.rules}/DERIVED_STATE_RULES.md` §4).
   Slug-Kollision mit bestehendem Ordner anderen Inhalts → melden und anderen Namen
   erfragen (kein Auto-Suffix, §4).
4. **Bestandsaufnahme des Change-Ordners** `{config.paths.workflows}/features/{slug}/`:
   - `fast-draft.md` vorhanden → **Wiederaufnahme anbieten** (Schritt 4) statt neu zu erheben
   - Vorhandene Artefakte (`discovery.md`, `spec.md`, `plan.md`) auflisten und **uebernehmen**:
     sie werden gelesen und NICHT neu erzeugt — vorbefuellt werden nur die fehlenden.
     Alle drei vorhanden → nichts zu tun, auf `/dtb:plan-review {slug}` verweisen
5. **INBOX-Status:** Hier noch KEIN Statuswechsel — der Flip auf `In Arbeit` passiert
   erst in Schritt 4 beim ersten Schreiben der fast-draft.md (E2E-Befund 2026-08-02:
   ein frueher Flip liesse eine sofort eskalierte Idee faelschlich als "In Arbeit" zurueck).

---

## Schritt 2: Struktur-Check (Kopplungs-Waechter)

Der Fast-Track traegt KEINE eigenen Templates — er liest die drei Quell-Skills als Single
Source. Vor jeder Erhebung pruefst du per Grep, ob die erwarteten Anker-Sektionen in den
**installierten Kopien** existieren:

| Template-Quelle (installierte Kopie) | Anker (Grep, woertlich) |
|--------------------------------------|-------------------------|
| `~/.claude/skills/dtb-feature-discover/SKILL.md` | `## Schritt 6` |
| `~/.claude/skills/dtb-feature-plan/SKILL.md` | `## Template fuer spec.md` |
| `~/.claude/skills/dtb-impl-plan/SKILL.md` | `## Template fuer plan.md` |

**Aufloesung je Quelle** (Muster wie `dtb:plan-review` Schritt 2): zuerst die installierte
Kopie `~/.claude/skills/dtb-*/SKILL.md`, sonst Fallback auf `skills/dtb-*/SKILL.md` im
Projekt-Root (Kit-Repo-Fall).

**Alle drei Anker gefunden** → eine Statuszeile ausgeben und weiter:
`🧩 Struktur-Check: 3/3 Template-Anker gefunden`

**Zwei getrennte Fehlerpfade** (nie vermischen — eine fehlende Installation ist KEINE Drift):

1. **Datei in beiden Quellen nicht gefunden** → Installations-Problem, kein Drift:

   ```
   ⚠ Template-Quelle {Skill} weder global (~/.claude/skills/) noch im Projekt gefunden.
      → /dtb:kit-sync sync ausfuehren (bzw. install), dann feature-fast erneut starten.
   ```

2. **Datei vorhanden, Anker fehlt** → Struktur-Drift, STOPP (kein Weiterarbeiten auf
   veralteter Basis):

   ```
   ⚠ Struktur-Check fehlgeschlagen: {Quelle} — Anker "{Anker}" nicht gefunden.
      Die Template-Quelle hat sich strukturell geaendert; ich buendele NICHT auf veralteter
      Basis. → dtb:feature-fast an die neue Struktur anpassen (die Wartungs-Hinweise an den
      Quell-Templates nennen diese Kopplung). Voll-Schiene als Ausweich: /dtb:feature-discover
   ```

> **Benanntes Restrisiko:** Der Check prueft Anker-EXISTENZ, nicht Template-INHALT. Gegen
> inhaltliche Drift verteidigen die Wartungs-Hinweise an den drei Quell-Templates — bei
> Aenderungen dort muss dieser Skill mitgezogen werden.

---

## Schritt 3: Erhebung (Defaults statt Interviews)

Ziel: Jeder Template-Abschnitt der drei Quellen ist vorbefuellt — mit belegten Fakten, wo
moeglich, und mit markierten Annahmen, wo nicht.

1. **Quellen lesen:** Idee-Text (+ dort verlinkte Artefakte), dann Repo-Kontext read-only
   erheben (Glob/Grep). Was du gegrept hast, ist ein **verifizierter Fakt** (Fundstelle
   merken); was du nur schliesst, ist eine **Vermutung** — die Trennung ist Pflicht
   (Lektion Inbox #36b: Auftraege/Vorlagen nennen verifizierte Fakten, Vermutungen sind
   explizit markiert).
2. **Templates lesen:** Die drei Anker-Sektionen aus Schritt 2 (Discovery-Template,
   Spec-Template inkl. Technical-Leak-Lint, Plan-Template inkl. `## Progress`-Format und
   Checkpoint-Kriterien-Regeln) sind die verbindliche Zielstruktur.
3. **Vorbefuellen:** Jeden Template-Abschnitt ausfuellen. Fuer `## Betroffene Module` gelten
   nur gegrepte, projekt-interne Pfade (keine Fremd-/Vorbildpfade). Der Plan-Entwurf haelt
   sich an alle impl-plan-Regeln (Automated/Manual-Kriterien, 3x3-Blockung, `## Progress`
   eine Zeile pro Schritt, Kopf `Status: Entwurf` im 10-Zeilen-Fenster nach §7).
4. **Annahmen nummerieren:** Jede nicht belegbare Angabe wird zur Annahme `A{n}` mit
   1-Satz-Begruendung und Kennzeichnung:
   - `✔` verifiziert — gegrepter Befund mit Fundstelle (zaehlt NICHT gegen das Budget)
   - `?` Vermutung — plausibel begruendet, aber unbelegt (zaehlt)
5. **Kernfragen-Budget (max. 3):** Nur wenn eine Kern-Annahme die ganze Vorlage kippen
   wuerde (Scope-Ziel, Zielort/Traeger, betroffener Nutzerkreis), stelle SOFORT eine
   gezielte Frage statt zu raten — hoechstens 3 fuer den gesamten Lauf, eine pro Nachricht.
   Alles andere bleibt Annahme und wird per Veto korrigierbar.
6. **Selbst-Eskalation (laufend pruefen):** Braucht der Entwurf **mehr als 10 Annahmen**
   oder **mehr als 2 Plan-Phasen**, ist die Idee kein Kleinfall:

   ```
   Kein Kleinfall: {N} Annahmen noetig / Plan braeuchte {M} Phasen (Schwellen: 10 / 2).
   Empfehlung: Voll-Schiene — /dtb:feature-discover {Nummer}
   Bereits Erhobenes geht nicht verloren: es fliesst als Startkontext in die Discovery.
   ```

   Der Nutzer entscheidet: wechseln (Empfehlung) oder bewusst im Fast-Track fortfahren.
   Das ist der **Eskalationspfad** — bereits geschriebene Artefakte bleiben in beiden
   Faellen gueltig.

---

## Schritt 4: Sammelvorlage (der eine Kontrollpunkt)

**Zuerst zwischenspeichern, dann fragen:** Schreibe die fertige Vorlage nach
`{config.paths.workflows}/features/{slug}/fast-draft.md` (Wiederaufnahme-Sicherung — die
Datei wird regulaer committet und reist im Zwei-Maschinen-Setup mit dem Ordner). Steht die
Idee noch auf `Offen`, setze sie JETZT auf `In Arbeit` — der Draft ist der Arbeitsbeginn
(bewusst erst hier, nicht in Schritt 1: sofort eskalierte Laeufe hinterlassen so keinen
falschen Status). Dann zeige sie im Chat:

```
# Fast-Track-Vorlage: {Feature-Name} (Inbox #{N})

## Kurzfassung je Artefakt
**discovery.md:** {3-5 Zeilen — Module, Scope-Kern, wichtigste Randfaelle}
**spec.md:**      {3-5 Zeilen — Ziel, Prioritaets-Vorschlag, Kern-Kriterien}
**plan.md:**      {3-5 Zeilen — Phasen (max. 2), Schrittzahl, Kern-Entscheidungen}

## Annahmen (einzeln vetobar, max. ~10)
A1 ? {Annahme} — {1-Satz-Begruendung}
A2 ✔ {Fakt} — {Fundstelle Pfad:Zeile}
...

Korrekturen als Freitext ("A2: stattdessen ..."), Unkommentiertes gilt als angenommen.
Ok zum Schreiben? (Ok / Korrekturen / Voll-Schiene / Abbruch)
```

**Regeln:**

- **Kurzfassung, nie voller Wortlaut** — die Artefakte selbst entstehen erst nach dem Ok
  und koennen dann im Detail gelesen werden. Braeuchte der Annahmen-Block mehr als ~10
  Eintraege, greift die Selbst-Eskalation aus Schritt 3.6 — keine ueberlange Vorlage bauen.
- **Veto-Verarbeitung:** Freitext-Korrekturen einarbeiten und NUR die geaenderten Annahmen
  kurz rueckbestaetigen (nicht die ganze Vorlage erneut zeigen). Kippt eine Korrektur den
  Scope-Kern → zurueck in die Erhebung (Schritt 3), fast-draft.md aktualisieren.
- **Antwort "Voll-Schiene"** → Eskalationspfad (Schritt 3.6): Verweis auf
  `/dtb:feature-discover {Nummer}`, Erhobenes bleibt als Startkontext erhalten.
- **Antwort "Abbruch"** → fast-draft.md bleibt liegen (bewusst — sie ist der
  Wiederaufnahme-Punkt), kein Artefakt wird geschrieben.
- **Wiederaufnahme** (Einstieg aus Schritt 1.4): Existiert beim Start eine `fast-draft.md`,
  biete an: (1) fortsetzen — Vorlage aus der Datei erneut zeigen, Vetos aufnehmen;
  (2) verwerfen — Datei loeschen (`rm .../fast-draft.md`, Bash) und neu erheben.
  Nie stillschweigend neu erheben.

---

## Schritt 5: Schreibphase (erst nach dem Ok)

1. **Reihenfolge fest:** `discovery.md` → `spec.md` → `plan.md` — so ist die
   Gate-Bedingung von impl-plan (spec.md existiert) im selben Lauf erfuellt.
2. **discovery.md** nach dem Schritt-6-Template der installierten feature-discover-Kopie
   (Resume-Marker final `<!-- resume: done -->`). Verbliebene `?`-Vermutungen, die der
   Nutzer nicht bestaetigt hat, werden als offene Punkte formuliert — nicht als Fakten.
3. **spec.md** nach dem Spec-Template der feature-plan-Kopie — inklusive
   **Technical-Leak-Lint**: Wende die Lint-Sektion der installierten feature-plan-Kopie an
   (Referenz, keine Kopie; Treffer → Hard-Block und korrigieren, wie dort definiert).
4. **plan.md** nach dem Plan-Template der impl-plan-Kopie: max. 2 Phasen, Automated/
   Manual-Checkpoint-Kriterien Pflicht, `## Progress` mit genau einer Zeile pro Schritt
   (§2), Kopfzeile `**Status:** Entwurf` im 10-Zeilen-Fenster (§7 — Pfleger ist und
   bleibt `dtb:plan-review`; dieser Skill fasst das Feld nach der Anlage NIE wieder an).
5. **Zwischenspeicher aufraeumen:** `fast-draft.md` loeschen — ihr Zweck ist erfuellt:
   `rm {config.paths.workflows}/features/{slug}/fast-draft.md` (Bash; Write kann nicht loeschen).
   **Keine A-IDs in den Artefakten:** Annahmen-Nummern (A1, A2, ...) leben nur in Vorlage
   und fast-draft.md — in den finalen Artefakten wird die Begruendung ausgeschrieben
   ("per Veto-Vorlage bestaetigt {Datum}"), sonst zeigen Belege nach dem Loeschen ins Leere.
   **Provenienz-Fusszeile (verbindlich):** Jedes der drei Artefakte endet auf
   `**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt {Datum})` —
   die bewusste Ausnahme von der Ununterscheidbarkeit (siehe "Wichtig").
6. **INBOX aktualisieren:** Idee auf `Ausgearbeitet`, Links anhaengen:
   `→ features/{slug}/discovery.md → features/{slug}/spec.md`

   **Teil-Guard (Worktree):** Laeuft dieser Skill in einem verlinkten Worktree
   (die Guard-Pruefung aus `skills/CLAUDE.md` → „Worktree-Guard (kanonische Vorlage)"
   meldet `WORKTREE`), Schritt 6 UND 7 NICHT ausfuehren — stattdessen genau eine
   Hinweiszeile `↷ INBOX.md-/BACKLOG.md-Update uebersprungen (Worktree) — in den Hand-off
   aufnehmen` und normal weiterarbeiten (Schreibgrenzen-Regel: `skills/CLAUDE.md` →
   „Parallele Sessions"). Gilt auch fuer den `In Arbeit`-Flip beim Start (Schritt 2/5).

7. **BACKLOG anbieten** (analog feature-plan Schritt 10). Bei Ja: Status-Spalte mit dem
   abgeleiteten Initial-Status **Geplant** eintragen (spec.md + plan.md existieren,
   0 Progress-Checkboxen — Regeln: `DERIVED_STATE_RULES.md`).
8. **Abschluss:**

   ```
   Fast-Track abgeschlossen: features/{slug}/ (discovery.md, spec.md, plan.md)

   Naechster Schritt: /dtb:plan-review {Feature-Name}
     (die Reviews laufen unveraendert — der Fast-Track verkuerzt nur die Erhebung)
   ```

---

## Wichtig

- **Erhebung verkuerzen, Absicherung nie:** Derived State, Hard-Gates, plan-review und
  impl-review gelten unveraendert; die erzeugten Artefakte muessen fuer die nachgelagerte
  Kette und die Statusableitung von Voll-Schienen-Artefakten ununterscheidbar sein —
  einzige bewusste Ausnahme ist die Provenienz-Fusszeile (Schritt 5.5)
- **INBOX ist Pflicht-Vorstufe** — kein Ad-hoc-Einstieg (Gate in Schritt 1)
- **Vor der Sammelvorlage hoechstens 3 Kernfragen**, danach entscheidet der Nutzer per
  Freitext-Veto — keine weiteren Interview-Runden
- **Groessen-Limits gelten weiter:** spec.md/plan.md max. 500 Zeilen
- **Deutsch:** Alle Texte auf Deutsch

## Verwandte Skills

- `/dtb:idea` / `/dtb:idea-review` — erfassen und triagieren die Idee (Weiche hierher)
- `/dtb:feature-discover` — Voll-Schiene (Eskalationsziel bei Nicht-Kleinfaellen)
- `/dtb:plan-review` — reviewt den erzeugten Plan (Nachfolger, unveraendert)
- `/dtb:implement` — setzt den reviewten Plan um (3x3 + Phasen-Ende-Ritual)
