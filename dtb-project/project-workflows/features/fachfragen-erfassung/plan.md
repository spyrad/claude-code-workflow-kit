# Implementierungsplan: Fachfragen-Erfassung

**Erstellt:** 2026-07-17
**Feature-Spec:** `features/fachfragen-erfassung/spec.md`
**Geschaetzte Dauer:** ~1,5 h
**Status:** Reviewed

---

## Phasen-Uebersicht

| Phase | Beschreibung | Dauer | Status |
|-------|-------------|-------|--------|
| Phase 1 | Konvention in DERIVED_STATE_RULES.md verankern (§6) | ~30 min | Geplant |
| Phase 2 | Schreibende Skills anleiten (feature-discover, feature-plan) | ~30 min | Geplant |
| Phase 3 | Folge-Idee erfassen & Doku | ~20 min | Geplant |

---

## Ist-Analyse

> Quelle: `discovery.md` (`## Betroffene Module`, Pfade verifiziert) + Grounding-Reads dieser Session.

| Pfad | Ist-Befund (relevant fuer den Plan) |
|------|-------------------------------------|
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §1–§5 + Fussnoten-Block (Z. 211–216). §2 zaehlt Checkboxen NUR in `## Progress`; §1.5 nur `## Schritte`/`## Fix-Schritte`. Neue §6 kommt nach §5 (Z. 209), vor den Fussnoten-Block. Kein bestehender `[Fach]`-Begriff. |
| `skills/dtb-feature-plan/SKILL.md` | Schreibt `## Offene Punkte` in `spec.md` (Template + harte „nie erfinden → als Frage eintragen"-Regel in Ausfuehrungs-Schritt 6). Kein `[Fach]`-Konzept. |
| `skills/dtb-feature-discover/SKILL.md` | Schreibt `## Offene Punkte` in `discovery.md` (Schritt-6-Template: „- [Falls waehrend der Discovery ungeklaerte Fragen aufkamen]"). Kein `[Fach]`-Konzept. |
| `CLAUDE.md` | Doku-Touch (Phase 3): Output-Locations/Konventionen — Ort fuer einen knappen `[Fach]`-Konventionshinweis. |

---

## Phase 1: Konvention in DERIVED_STATE_RULES.md verankern

### Ziel
Die `[Fach]`-Konvention zentral und eindeutig als Ableitungsregel festschreiben — Fundament, auf das die Skills (Phase 2) und die spaetere Lese-Ansicht verweisen. Kollision mit der Kern-Statusableitung ausschliessen.

### Schritte

#### Schritt 1.1: §6 Regeltext — Tag-Grammatik & Antwort-Format
- **Zweck:** Verbindliche Form der Fach-Frage definieren.
- **Dateien:** `dtb-project/project-rules/DERIVED_STATE_RULES.md` (neue Sektion `## 6. Fach-Frage-Konvention (Offene Punkte)` nach §5)
- **Input:** Design-Entscheidung B (Inline-Tag), Spec-Scope
- **Output:** Grammatik `- [ ] [Fach] {Frage}` in `## Offene Punkte`; Antwort-Nachtrag-Format (eingerueckter Zusatz `→ Antwort: … (Meeting YYYY-MM-DD)` unter dem abgehakten Bullet, Eintrag bleibt als Beleg stehen). Die Grammatik gilt **dateiunabhaengig** fuer JEDES `## Offene Punkte` (unabhaengig von der Datei), damit die spaetere Lese-Ansicht konsistent scannen kann.

#### Schritt 1.2: §6 Status-Neutralitaet, Ableitung & Rueckwaertskompatibilitaet
- **Zweck:** Die zentrale Kollisionsgefahr bannen — eine `## Offene Punkte`-Checkbox ist **status-neutral** und zaehlt NICHT fuer §1/§2 (nur `## Progress`/`## Schritte`/`## Fix-Schritte` speisen die Ableitung, analog `review.md`).
- **Dateien:** `DERIVED_STATE_RULES.md` (§6, Fortsetzung)
- **Input:** §1.1/§2/§1.5 (Grounding: welche Sektionen die Ableitung speisen)
- **Output:** Explizite Klarstellung „Fach-Frage-Checkboxen sind status-neutral"; Ableitung Fach-Frage `[ ]`=offen / `[x]`=beantwortet (nur fuer die spaetere Agenda-Lese-Ansicht); Rueckwaertskompatibilitaet: Bullet ohne `[Fach]`-Tag = normaler „selbst-zu-klaeren"-Punkt, bleibt gueltig. Zusatz: der `implement`-Loop und die Statusableitung bleiben **blind** gegen `## Offene Punkte`-Checkboxen — nur `## Progress`/`## Schritte`/`## Fix-Schritte` speisen die Ableitung.

#### Schritt 1.3: Fussnoten-Block ergaenzen
- **Zweck:** Herkunft dokumentieren + bekannten Seed-Skew markieren.
- **Dateien:** `DERIVED_STATE_RULES.md` (Fussnoten-Block Z. 211 ff.)
- **Input:** bestehendes Fussnoten-Muster
- **Output:** Zeile „**§6 Fach-Frage-Konvention ergaenzt:** Feature fachfragen-erfassung, 2026-07-17 (Seed-Aenderung — erreicht Bestandsprojekte nicht automatisch, vgl. INBOX #22)".

> **3x3-Block:** Nach Schritt 1.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] Neue `## 6.`-Sektion in `DERIVED_STATE_RULES.md` mit Grammatik, Status-Neutralitaet, Ableitung, Rueckwaertskompat, Antwort-Format
- [ ] Fussnoten-Zeile ergaenzt

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -n "## 6" dtb-project/project-rules/DERIVED_STATE_RULES.md` liefert die neue Sektion
- [ ] `grep -n "\[Fach\]" dtb-project/project-rules/DERIVED_STATE_RULES.md` liefert Treffer
- [ ] `grep -n "status-neutral" dtb-project/project-rules/DERIVED_STATE_RULES.md` belegt die Abgrenzung zu §1/§2

#### Manual
- [ ] §6 deckt alle vier Aspekte (Grammatik, Status-Neutralitaet, Ableitung offen/beantwortet, Rueckwaertskompat) widerspruchsfrei zu §1/§2 ab

---

## Phase 2: Schreibende Skills anleiten

### Ziel
`feature-discover` und `feature-plan` weisen aktiv an, geeignete offene Fragen als `[Fach]` zu erfassen — mit Verweis auf §6. Kein Zwang, keine Erfindung: nur echte, nicht sofort/allein beantwortbare Fragen.

### Schritte

#### Schritt 2.1: feature-discover anleiten
- **Zweck:** Fach-Fragen bereits in der Discovery erfassbar machen.
- **Dateien:** `skills/dtb-feature-discover/SKILL.md` (Schritt-6-Template `## Offene Punkte` + kurze Anleitung)
- **Input:** §6 aus Phase 1
- **Output:** Template-Beispiel zeigt `- [ ] [Fach] {Frage}`; Anleitungssatz „Frage, die ins Fach-Meeting gehoert (nicht sofort/allein beantwortbar) → als `[Fach]` markieren; sonst normaler Bullet". **Degradationsfest:** Anleitung + Beispiel sind selbsterklaerend im Skill; §6 nur als Kanon-/Detail-Verweis (nicht Pflichtlektuere), damit ein Zielprojekt ohne §6-Seed nicht auf eine tote Referenz zeigt.

#### Schritt 2.2: feature-plan anleiten
- **Zweck:** Gleiche Konvention beim Spec-Schreiben; koppelt an die bestehende „nie erfinden"-Regel.
- **Dateien:** `skills/dtb-feature-plan/SKILL.md` (Template `## Offene Punkte` + Ausfuehrungs-Schritt 6 „nie erfinden")
- **Input:** §6, bestehende „nie erfinden"-Regel
- **Output:** Template-Beispiel `- [ ] [Fach] {Frage}`; **degradationsfest** (selbsterklaerend, §6 nur Kanon-Verweis). Die drei Faelle explizit trennen: (a) normaler offener Punkt = untagged Bullet, selbst zu klaeren; (b) „nie erfinden"-Luecke = fehlende Info als Frage, oft selbst/in der Spec klaerbar; (c) `[Fach]`-Frage = gehoert ins Fach-Meeting (nicht sofort/allein beantwortbar). Nur (c) traegt den Tag.

#### Schritt 2.3: Konsistenz-, Unterscheidbarkeits- & Verhaltens-Beleg
- **Zweck:** Beweisen, dass die Konvention einheitlich referenziert ist, maschinell unterscheidbar (SC3), Bestand nicht bricht und die Anleitung real greift.
- **Dateien:** keine (nicht-mutierender Verifikationsschritt)
- **Input:** geaenderte Skills + reale Bestands-Artefakte (inkl. Dogfood-Beispiel `- [ ] [Fach] Prioritaet bestaetigen` in `features/fachfragen-erfassung/spec.md`)
- **Output:**
  - **(a) Konsistenz:** Grep-Beleg, dass beide Skills `[Fach]` + §6-Verweis tragen; Beleg an ≥1 bestehendem untagged `## Offene Punkte`-Bullet, dass es weiterhin als gueltiger „selbst-zu-klaeren"-Punkt gilt (keine Migration noetig).
  - **(b) Unterscheidbarkeit (SC3):** `grep '\[Fach\]' features/*/spec.md` findet die getaggte Zeile, untagged Bullets nicht — belegt die maschinelle Unterscheidbarkeit an einem echten Vorkommen.
  - **(c) Verhaltens-Beleg (Trockenlauf):** ein beobachteter Trockenlauf, dass `feature-discover`/`feature-plan` bei einer Meeting-tauglichen Frage real einen `[Fach]`-Bullet erzeugt — und dabei die Kollision „nie erfinden"-Luecke vs. `[Fach]`-Meeting-Frage sauber getrennt bleibt (Lektion #5).

> **3x3-Block:** Nach Schritt 2.3 → Zusammenfassung + Feedback einholen

### Deliverables
- [ ] `feature-discover` + `feature-plan` mit `[Fach]`-Anleitung und §6-Verweis
- [ ] Beleg der Rueckwaertskompatibilitaet (untagged Bullets bleiben gueltig)

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -l "\[Fach\]" skills/dtb-feature-discover/SKILL.md skills/dtb-feature-plan/SKILL.md` listet beide Dateien
- [ ] Beide Skills verweisen auf `DERIVED_STATE_RULES.md` §6 (grep „§6" bzw. „Fach-Frage-Konvention")
- [ ] `grep '\[Fach\]' features/*/spec.md` findet die getaggte Zeile (SC3-Unterscheidbarkeit an echtem Vorkommen)

#### Manual
- [ ] Anleitung ist aktiv formuliert (Autor wird zur Markierung angeleitet), nicht nur eine Doku-Fussnote; der untagged-Fall bleibt sichtbar zulaessig; die drei Faelle (untagged / „nie erfinden" / `[Fach]`) sind getrennt
- [ ] Beobachteter Trockenlauf: eine Meeting-taugliche Frage erzeugt real einen `[Fach]`-Bullet, „nie erfinden"-Luecke bleibt davon getrennt

---

## Phase 3: Folge-Idee erfassen & Doku

### Ziel
Die ausgelagerte Lese-Ansicht als konkrete Folge-Idee sichern und die Konvention in der Projekt-Doku auffindbar machen.

### Schritte

#### Schritt 3.1: Folge-Idee in INBOX
- **Zweck:** Die Meeting-Agenda-Lese-Ansicht darf nicht verloren gehen (Success Criterion).
- **Dateien:** `dtb-project/project-workflows/INBOX.md`
- **Input:** Spec-Scope „Nicht enthalten" + Offene Punkte
- **Output:** Neuer INBOX-Eintrag (Status `Offen`): rein-lesender Skill (z.B. `/dtb:fach-agenda`), sammelt offene `[Fach]`-Fragen aus `features/*/{discovery,spec,plan}.md`, gruppiert pro Feature → Meeting-Agenda; `produces: []`; abzugrenzen von #24 (Antwort-Rueckfluss). Verweis auf §6 als Konsum-Konvention.

#### Schritt 3.2: Doku-Hinweis
- **Zweck:** Konvention in der Kit-Doku auffindbar machen.
- **Dateien:** `CLAUDE.md` (Abschnitt Output-Locations bzw. Konventionen)
- **Input:** §6
- **Output:** Knapper Hinweis, dass offene Fragen fuers Fach-Meeting als `- [ ] [Fach] …` in `## Offene Punkte` erfasst werden (Regel: `DERIVED_STATE_RULES.md` §6).

### Deliverables
- [ ] INBOX-Folge-Idee angelegt
- [ ] CLAUDE.md-Konventionshinweis ergaenzt

### Checkpoint-Kriterien

#### Automated
- [ ] `grep -n "\[Fach\]" dtb-project/project-workflows/INBOX.md` liefert den neuen Eintrag
- [ ] `grep -n "\[Fach\]" CLAUDE.md` liefert den Doku-Hinweis

---

## Technische Entscheidungen

| Thema | Optionen | Entscheidung | Begruendung |
|-------|----------|-------------|-------------|
| Verortung der Regel | eigene Regel-Datei / §6 in DERIVED_STATE_RULES.md | §6 in DERIVED_STATE_RULES.md | Es ist eine Ableitungs-/Statuskonvention; gehoert zur „Single Source fuer Statusableitung" |
| Tag-Syntax | Inline `[Fach]` / eigene `## Fachfragen`-Sektion | Inline `[Fach]` (Entscheidung B) | Ein Ort, rueckwaertskompatibel, per Tag unterscheidbar |
| Reichweite | discovery+spec / +plan (impl-plan) | nur discovery+spec (Entscheidung A) | Fach-Fragen entstehen im Was/Warum; kleiner Scope, impl-plan unberuehrt |
| Status-Neutralitaet der Offene-Punkte-Checkbox | zaehlt fuer Ableitung / status-neutral | status-neutral | Verhindert Verwechslung mit `## Progress`; analog `review.md` |
| Zweite Tag-Variante `[Stakeholder]` | jetzt / spaeter | spaeter (nicht MVP) | Scope schlank halten; erst Bedarf belegen |
| §6-Verweis vs. Seed-Skew | degradationsfest / §6 harte Voraussetzung | degradationsfest | §6 ist Klasse-B-Seed (#22); Skill-Anleitung selbsterklaerend, §6 nur Kanon → Bestandsprojekt bricht nicht, Scope bleibt bei diesem Feature |
| §6-Geltungsbereich | an feste Datei gebunden / dateiunabhaengig | dateiunabhaengig | gilt fuer jedes `## Offene Punkte`; haelt spaetere Lese-Ansicht konsistent |
| Test-Beleg | nur statisch (grep) / + beobachteter Trockenlauf | + Trockenlauf | grep belegt Textpraesenz, nicht Wirkung; Trockenlauf testet reale Erfassung + Kollision „nie erfinden" vs. `[Fach]` (Lektion #5) |

---

## Progress

> Single Source of Truth fuer den Umsetzungsstand (Regeln: `project-rules/DERIVED_STATE_RULES.md`).
> Abhaken gemaess Flip-Bedingung §2 (Automated-Kriterien der Phase gruen); SHA-Nachtrag beim
> Phasen-Ende-Commit — geflippte Zeile ohne SHA ist mid-phase gueltig (§2 Regel 4).

- [x] 1.1 §6 Regeltext (Grammatik & Antwort-Format) — `8dd722c`
- [x] 1.2 §6 Status-Neutralitaet, Ableitung & Rueckwaertskompat — `8dd722c`
- [x] 1.3 Fussnoten-Block ergaenzt — `8dd722c`
- [x] 2.1 feature-discover anleiten — `5ab2987`
- [x] 2.2 feature-plan anleiten — `5ab2987`
- [x] 2.3 Konsistenz- & Rueckwaertskompat-Beleg — `5ab2987`
- [x] 3.1 Folge-Idee in INBOX
- [x] 3.2 Doku-Hinweis (CLAUDE.md)

---

## Umsetzung

Umsetzung mit `/dtb:implement fachfragen-erfassung` — 3x3-Rhythmus und Phasen-Ende-Ritual
(Verifikations-Gate, SHA-Nachtrag) sind dort beschrieben (die eine Quelle).
Wiedereinstieg bei Kontextverlust: `features/fachfragen-erfassung/plan.md` laden; der erste nicht
abgehakte Schritt in `## Progress` ist der naechste.
Erkenntnisse/Abweichungen gehoeren in den Session-Log (`/dtb:workflow-checkpoint`).

---

**Erstellt mit:** `/dtb:impl-plan`
