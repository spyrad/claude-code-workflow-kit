# Feature: Capture-Duplikat-Schutz

**Erstellt:** 2026-08-19
**Ziel:** Die drei ungeschuetzten Capture-Skills des Grundbestands (`idea`, `task`, `bug-report`) pruefen vor dem Schreiben auf eine inhaltliche Dublette — getragen von einer Konvention, die auch jeder kuenftige Capture-Skill erbt.
**Prioritaet:** Mittel
**Status:** Fertig zum Testen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Drei der sechs Capture-Skills pruefen vor dem Schreiben auf eine Dublette, drei nicht — und die
Trennlinie ist kein Zufall: die geschuetzten entstanden je in einem eigenen Feature, die
ungeschuetzten gehoeren zum Grundbestand und wurden nie nachgezogen. Dieses Feature schliesst die
Luecke nicht nur an den drei Fundstellen, sondern hebt die Regel in eine Autoren-Konvention, damit
der siebte Capture-Skill sie nicht erneut erbt.

Der Schmerz ist latent, nicht akut: ein dokumentierter Beinahe-Fall (2026-08-06), keine tatsaechliche
Dublette im Bestand. Der Wert liegt darin, dass eine Dublette **spaet** auffaellt — die Nummern der
Ideen-Sammlung sind im Kit Zitierschluessel, und zwei Nummern fuer einen Sachverhalt gabeln die
Referenz-Spur dauerhaft, ohne dass eine der beiden Haelften vollstaendig bleibt.

---

## Scope / Abgrenzung

### Enthalten

**1. Autoren-Konvention in `skills/CLAUDE.md`** — in der Form der bestehenden
`Eligibility-Gates`-Sektion (geteilte Mechanik zentral, pro Skill eine verbindliche Tabellenzeile),
**nicht** in der Form des Worktree-Guards (byte-identische Kopie). Grund: der Guard ist kopierbar,
weil sein Kern fuer alle Skills wortgleich ist; der Duplikat-Check ist es nicht — jedes Ziel hat
einen eigenen Suchraum. Geteilt sind nur Kriterium, Meldeform und Einteilungsregel. Die Sektion
enthaelt:

- **Einteilungsregel** mit mechanisch pruefbarem Kriterium (Vorbild: die `produces:`-Pruefung der
  Guard-Kategorien, „mechanisch pruefen, nie schaetzen"). Richtung: *erfasst einen vom Menschen
  formulierten Freitext-Eintrag in eine Sammel-Datei, ohne vorher eine Identitaet zu vergeben*.
- **Kopplungsregel Meldeform ↔ Vergleichsschaerfe:**
  > Unscharfer Vergleich → **Treffer melden und fragen** (Ja/Abbrechen), nie selbst entscheiden.
  > Exakter Vergleich → **melden und ueberspringen** ist zulaessig, weil ein Falsch-Positiv
  > ausgeschlossen ist.

  Begruendung unabhaengig vom Bestand: ein unscharfer Vergleich hat Falsch-Positive per
  Konstruktion, ein Mechanismus der sich irren kann darf nicht allein entscheiden; ein exakter
  Vergleich hat keine, die Rueckfrage waere Zeremonie. **Nebeneffekt:** die zwei abweichenden
  Meldeformen im Bestand (`lesson` fragt, `open-question` ueberspringt) werden dadurch *erklaert*,
  nicht geaendert.
- **Meldeform-Schema mit benannten Slots** (Fundstelle → Bestandstext → Entscheidungsfrage) statt
  eines woertlich zu spiegelnden Textes. Die erste Zeile muss pro Skill abweichen; jeder weitere
  woertliche Spiegel waere Wartungsschuld.
- **Verbindliche Zuordnungstabelle** mit **allen sechs** Capture-Skills — auch den drei bereits
  geschuetzten. Eine Tabelle mit nur der Haelfte der Faelle wird in vier Wochen unvollstaendig
  gelesen.
- **Abgrenzung zur Slug-Kollision:** Namens-Kollision ist in `DERIVED_STATE_RULES.md` §4 geregelt,
  Inhalts-Dublette ist der neue Fall. Beide koennen gleichzeitig auftreten.

**2. Die Ersetzungsprobe wird zum Kanon gehoben — mit deklariertem Laufzeit-Spiegel.** Sie existiert
heute genau einmal, inline in `dtb:no-loss-check`; kein anderer Ort verweist darauf. Der verbindliche
Wortlaut samt Begruendung zieht nach `skills/CLAUDE.md`; der Skill behaelt eine **vollstaendige
operative Fassung** samt eigenen Beispielen (installierte Skills laufen in Zielprojekten, wo
`skills/CLAUDE.md` nicht existiert — ein blosser Verweis braeche die Laufzeit). Beide Stellen tragen
Kopplungs-Hinweise in je ihre Richtung (Muster: Worktree-Guard — Vorlage im Guide, operative Fassung
im Skill, Spiegel-Verifikation dazwischen). Das Kit hat den Hebe-Zug bereits gemacht (L7/L8/L14
wurden 2026-07-31 dorthin gehoben) und `dtb:lesson` empfiehlt ihn ausdruecklich.

**3. Haertung der drei Zielskills** nach dieser Konvention:

- eine Sektion mit dem Anker `## Duplikat-Check`, **bewusst ohne Schritt-Nummer** — die Skills haben
  unterschiedlich viele Schritte (3 / 6 / 6), eine feste Nummer kann es nicht geben; Begruendung
  analog Worktree-Guard („eine zweite Null waere ambig")
- **Position:** nach der Erfassung, vor dem ersten Schreiben (anders als der Guard, der ganz vorne
  sitzt — der Check braucht den erfassten Text)
- bei `task`/`bug-report` **vor** der Slug-Vergabe: bei erkanntem Duplikat braucht es keinen Namen
- **Stoerungsfreiheit bleibt das Versprechen: kein Treffer → keine Ausgabe.** Keine
  Bestaetigungszeile, kein „Check: ok". Alle drei Skills versprechen ausdruecklich Stoerungsfreiheit;
  das Versprechen darf nirgends relativiert werden. Wortlaut-Vorbild ist der Guard („im Normalfall
  unsichtbar").
- `dtb:idea` braucht dafuer eine **Frontmatter-Aenderung** (die Stichwort-Suche ist in seinen
  deklarierten Werkzeugen nicht enthalten — der einzige der sechs, dem sie fehlt)

**4. Abschluss-Schritt:** drei verteilte Artefakte aendern sich, die Drift-Erkennung meldet die
installierten Kopien → `dtb:kit-sync` gehoert zum Feature, nicht in die Nacharbeit.

### Nicht enthalten

- **Kein Umbau** an `lesson`, `open-question`, `meeting-dump` — sie kommen nur in die
  Zuordnungstabelle; ihre bestehenden Formen werden durch die Kopplungsregel erklaert.
  (`no-loss-check` ist die eine Ausnahme: es wird deklarierter Spiegel des Kanons —
  Kopplungs-Hinweis kommt hinzu, seine Logik und Beispiele bleiben.)
- **Kein hartes Blocken** — bei unscharfem Vergleich entscheidet immer der Mensch.
- **Kein Durchsuchen von `archive/`.** Kit-konform (drei bestehende Skills schliessen es ebenso aus)
  und sachlich begruendet: Wiederkehr ist bei Housekeeping-Aufgaben normal, ein Treffer dort waere
  meist ein Falsch-Positiv. **Bewusst akzeptierte Restluecke:** die Wiedererfassung einer schon
  umgesetzten Sache wird nicht erkannt — bei `idea` real belegt (die Eintraege #29 und #42 sind aus
  der Sammel-Datei verschwunden, ein erneutes Erfassen liefe kommentarlos durch).
- **Keine Regressions-Erkennung** fuer `bug-report` (gleiches Symptom + geschlossener Bug = Signal,
  nicht Dublette) — eigenes Feature, als Folge-Idee zu erfassen.
- **Keine Aenderung an §4** der Statusableitungs-Regeln — die Slug-Kollision bleibt wie sie ist, die
  Abgrenzung wird nur benannt.
- **Kein Aufraeumen des Bestands** — vorhandene Dubletten werden nicht nachbearbeitet.
- **Keine Aenderung am `pipeline:`-Block** der drei Skills → die Pipeline-Ansichten bleiben unberuehrt.

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| **Die Konvention wird nicht eingehalten** — der naechste Capture-Skill erbt die Luecke doch. Das ist der Hauptzweck des Features; `dtb:impl-review` liest `skills/CLAUDE.md` nicht | Mittel | Hoch | Einhaltung mechanisch verankern statt im Fliesstext: Anker-Suche mit Zielzahl + `dtb:project-health` + vollstaendige Zuordnungstabelle (kein „…" am Tabellenende) |
| **Der Worktree-Guard-Block in `dtb:idea` wird beim Einfuegen veraendert** — `idea` ist die benannte Referenz-Instanz, jede Abweichung ist ein Befund und reist ueber die Verteilung mit | Niedrig | Hoch | Die neue Sektion strikt NACH dem Guard einfuegen; Guard-Block und Abbruch-Fence als unveraendert belegen |
| **Kein natuerlicher Belegfall fuer `task`/`bug-report`** — aktive Changes haben derzeit 0 Aufgaben- und 0 Bug-Dateien; das Feature koennte ohne Nachweis abgenommen werden | Hoch | Mittel | E2E-Beleg mit **angelegter** Test-Situation je Skill (Treffer- und Blind-Lauf), Test-Artefakte danach zuruecknehmen; der Beleg ist Teil des Plans, nicht der Nacharbeit |
| **Ungekoppelte Wortlaute der Ersetzungsprobe** (Kanon und Skill-Fassung driften auseinander) — die Wartungsschuld, die die Spiegel-Regel adressiert; ein reiner Verweis statt Spiegel schied aus (Laufzeit-Autarkie installierter Skills) | Mittel | Mittel | Deklarierte Spiegel-Konstruktion mit Kopplungs-Hinweisen in beide Richtungen; Verifikation per Kern-Wortlaut-Suche mit Zielzahl 2 (keine dritte Stelle) |
| **Falsch-Positive nerven und kippen das Stoerungsfreiheits-Versprechen** | Mittel | Mittel | Kein Treffer → keine Ausgabe; Treffer immer als Frage (Ja/Abbrechen), nie als Entscheidung; Ersetzungsprobe statt Prozent-Schwelle (eine Quote suggeriert Messbarkeit, die nicht existiert) |
| **Frontmatter-Nachzug bei `dtb:idea` vergessen** → der Check laeuft ins Leere | Niedrig | Hoch | `dtb:project-health` prueft den Skill-Rumpf gegen die deklarierten Werkzeuge und warnt automatisch — als Abnahme-Schritt einplanen |
| **Zusammenfuehr-Konflikt in `skills/CLAUDE.md`** — heisseste Datei des Repos, zuletzt am selben Tag geaendert | Niedrig | Mittel | Aktuell existiert kein zweiter Feature-Arbeitsplatz; vor Beginn und vor der Rueckgabe den Stand abgleichen, frueh zusammenfuehren |
| **Zeilennummern-Belege der Discovery veralten** | Mittel | Niedrig | In Spec und Plan ueber **Anker-Text** verweisen, nicht ueber Zeilennummern |

---

## Dependencies

### Erforderlich vor Start
- [ ] Kein zweiter Schreiber an `skills/CLAUDE.md` (Arbeitsplatz-Liste pruefen und mit der
      Orchestrator-Session abgleichen) — aktuell erfuellt
- [ ] Getragen, dass `no-loss-check` als **deklarierter Spiegel des Kanons** in den Scope kommt
      (Discovery entschied „heben"; das Review praezisierte auf Kanon + Laufzeit-Spiegel, weil
      installierte Skills ohne `skills/CLAUDE.md` laufen)

### Referenz-Dokumente
- `features/capture-duplikat-schutz/discovery.md` — Erhebung mit allen fuenf Entscheidungen, Belegen
  und der Modul-Liste
- `skills/CLAUDE.md`, Sektion „Eligibility-Gates" — **Formvorbild** der neuen Konvention
- `skills/CLAUDE.md`, Sektion „Worktree-Guard (kanonische Vorlage)" — Gegenvorbild (byte-identische
  Kopie) und Quelle des Prinzips „im Normalfall unsichtbar"
- `skills/CLAUDE.md`, Sektion „Kopplungs-Hinweise: Spiegel mitziehen und verifizieren" — verlangt
  die Verifikation mit Zielzahl
- `skills/dtb-no-loss-check/SKILL.md`, Sektion „Die Unterdrueckungs-Regel: Ersetzungsprobe" —
  zu hebender Kanon
- `skills/dtb-lesson/SKILL.md` — Vorlage der Meldeform (von der Ursprungs-Idee als 1:1-Vorlage
  benannt)
- `skills/dtb-open-question/SKILL.md`, `skills/dtb-meeting-dump/SKILL.md` — die beiden anderen
  Bestandsformen, die die Kopplungsregel erklaeren muss
- `skills/dtb-project-health/SKILL.md` — mechanischer Verifizierer des Frontmatter-Nachzugs
- `skills/dtb-kit-sync/SKILL.md` — Klassen-Tabelle: die Konvention selbst wird **nicht** verteilt
  (Contributor-Guide), die Wirkung reist ueber die drei gehaerteten Skill-Dateien
- `dtb-project/project-rules/DERIVED_STATE_RULES.md` §4 — Slug-Kollision, Abgrenzung zur
  Inhalts-Dublette

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**

- [ ] Die Konventions-Sektion in `skills/CLAUDE.md` existiert und enthaelt alle fuenf Bestandteile:
      Einteilungsregel mit pruefbarem Kriterium, Kopplungsregel, Meldeform-Schema, vollstaendige
      Zuordnungstabelle (**sechs** Capture-Skills), Abgrenzung zur Slug-Kollision
- [ ] Die Ersetzungsprobe hat **genau eine kanonische Fassung** (`skills/CLAUDE.md`) plus **einen
      deklarierten Spiegel** (`dtb:no-loss-check`, operative Fassung mit behaltenen Beispielen);
      beide tragen Kopplungs-Hinweise — die Suche nach dem Kern-Wortlaut trifft genau diese zwei
      Stellen, keine dritte
- [ ] Alle drei Zielskills tragen die Ankerzeile `## Duplikat-Check`; die Anker-Suche erreicht die
      Zielzahl aus der Zuordnungstabelle
- [ ] `dtb:idea` deklariert die Stichwort-Suche in seinen Werkzeugen; `dtb:project-health` meldet fuer
      keinen der drei Skills eine Werkzeug-Warnung
- [ ] **Blind-Lauf je Skill belegt** (als Mechanik-Beleg in dieser Session; der echte Skill-Lauf
      folgt nach dem Zusammenfuehren im Haupt-Checkout — Voll-Guard): ohne Treffer erscheint keine
      Zeile, das Stoerungsfreiheits-Versprechen ist messbar unveraendert
- [ ] **Treffer-Lauf je Skill belegt** (Beleg-Art wie beim Blind-Lauf): Fundstelle genannt,
      Bestandstext gekuerzt, Entscheidung beim Menschen (Ja/Abbrechen); bei `task`/`bug-report` lief
      der Check vor der Namensvergabe
- [ ] Der Worktree-Guard-Block in `dtb:idea` ist unveraendert (Vergleich belegt)
- [ ] `archive/` wird von keinem der drei Checks durchsucht (belegt)
- [ ] Die Uebergabe-Notiz benennt `dtb:kit-sync` als ersten Orchestrator-Schritt nach dem
      Zusammenfuehren (die Drift-Aufloesung selbst kann dieser Arbeitsplatz strukturell nicht
      leisten — `kit-sync` hat keinen Worktree-Guard und wuerde hier den Branch-Stand global
      installieren)
- [ ] Die drei bereits geschuetzten Skills sind unveraendert (ausser dem Spiegel-/Kopplungs-Hinweis
      in `no-loss-check`) — Vergleich belegt

---

## Offene Punkte

- Wortlaut der Einteilungsregel: das Kriterium ist richtungsentschieden (*Freitext-Eintrag in eine
  Sammel-Datei ohne vorher vergebene Identitaet*), die verbindliche Formulierung entsteht bei der
  Umsetzung. Sie muss so scharf sein, dass sie ohne Ermessen ueber einen neuen Skill entscheidet.
- Die Einhaltung der Konvention haengt an Anker-Suche und `dtb:project-health` — `dtb:impl-review`
  liest `skills/CLAUDE.md` nicht. Das gilt heute fuer alle Mechanik-Regeln dort und ist kein neues
  Problem, bleibt aber die schwaechste Stelle des Features. Ob das genuegt oder ein Review-Schritt
  nachgezogen werden sollte, ist nicht entschieden.
- **Folge-Idee, vom Orchestrator zu erfassen** (in diesem Arbeitsplatz nicht moeglich):
  Regressions-Erkennung fuer `bug-report` — ein Treffer im Archiv auf gleiches Symptom bei
  geschlossenem Bug ist ein Signal, keine Dublette. Bewusst aus diesem Feature ausgeschlossen.

---

**Erstellt mit:** `/dtb:feature-plan`
