# Discovery: Checkpoint ohne Rueckfragen
<!-- resume: done -->

**Erstellt:** 2026-11-03
**Idee-Referenz:** Inbox #173 — "Checkpoint ohne Rückfragen bei Verlustfunden und offenen Aufgaben" (Nachtrag: Becken #185 — Weglassen braucht eine bewusste Aenderung von `DERIVED_STATE_RULES.md` §9.4)
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-workflow-checkpoint/SKILL.md` | Kern: Schritt 0 (Funde erfassen), Schritt 1 (Aufgaben-Vergleich, ⏳ Alter, `#### Kontrollpunkt` A/B/C mit Antwortregeln), Pfeil-Slot im Session-Log-Format |
| `dtb-project/project-rules/DERIVED_STATE_RULES.md` | §9.2/§9.3 (Rueckfragen Zuordnung/Abgang), §9.4 (⏳-Sammelvorlage, „nie automatisch", „Eine Rueckfrage-Runde") + Aenderungs-Absatz am Ende |
| `skills/dtb-no-loss-check/SKILL.md` | Gruppen „Vor dem Checkpoint erledigen" / „Kann warten", Format-Kopplung zum Checkpoint |
| `skills/CLAUDE.md` | Rueckfragen-Defaults-Tabelle Zeile I (Kontrollpunkt), Schreibgrenzen-Tabelle |
| `CLAUDE.md` | Kit-Beschreibung von `workflow-checkpoint` (Kontrollpunkt, ⏳-Vorlage, Teil A/B/C) |
| `skills/dtb-lesson/SKILL.md` | Kopplungs-Hinweise „Kontrollpunkt Teil A" |
| `skills/dtb-idea/SKILL.md` | Kopplungs-Hinweise „Kontrollpunkt Teil A" |
| `skills/dtb-idea-triage/SKILL.md` | Kopplungs-Hinweise Teil A, Becken-Schreibmechanik |
| `skills/dtb-project-dashboard/SKILL.md` | zeigt ⏳ / offene Aufgaben (liest §9-Format) |
| `dtb-project/project-workflows/features/checkpoint-schneller/` | Vorgaenger #177: Kontrollpunkt-Design, Nachmessung bis 2026-12-02 |

---

## Anforderungen

### Scope
**Enthalten:**
- **Verlustfunde ohne Rueckfrage:** dringende Lektionen und Ideen („Vor dem Checkpoint erledigen") werden direkt erfasst; Ideen aus „Kann warten" gehen still ins Becken `INBOX-BEFUNDE.md` (Entscheidung #75 bleibt). Anzeige danach nur als Meldezeilen (`✔ L{N} → lessons.md`, `✔ #{N} → INBOX-BEFUNDE.md`)
- **Alte offene Aufgaben (⏳) automatisch behalten:** keine Sammelvorlage mehr, eine Anzeigezeile (`⏳ {K} Aufgaben ≥ {S} Tage — behalten`) — bewusste Aenderung von §9.4 („nie automatisch")
- Folge: im Normalfall laeuft der Checkpoint ganz ohne Rueckfrage durch

**Nicht enthalten:**
- **Unsichere Aufgaben-Zuordnung bleibt eine Frage** („ist X = Y?", „X erledigt? — Hinweis ohne Beleg"): hier steht echte Information auf dem Spiel (stille Dublette bzw. stilles Streichen); kommt selten
- Abnahme-Frage (Schritt 2) und fehlende Hand-off-Pflichtfelder bleiben eigene Fragen

### Gewuenschtes Verhalten
- **Meldezeilen gesammelt in der Abschlussbestaetigung** (Schritt 6), nicht verstreut waehrend des Laufs — alles an einer Stelle
- **Je erfasster Lektion der Rule-Satz gekuerzt in der Meldung**, nicht nur die Nummer — ohne Vorab-Bestaetigung muss sichtbar sein, was jetzt als Prior fuer die Planungs-Skills gilt
- **⏳ bleibt einfach stehen:** faellige Aufgaben behalten die ⏳-Markierung am Zeilenende, keine Frage, KEIN automatischer `· behalten`-Stempel — sonst verschwaende ⏳ alle `alter_schwelle_tage` still und das Warnzeichen waere wirkungslos. Erledigen/Verwerfen bleibt jederzeit per Session-Signal moeglich (Abgangsvermerk §9.3)
- Umgedeutet gegenueber #185 („alte Aufgaben automatisch behalten"): behalten heisst hier „weitertragen mit ⏳", nicht „Stempel setzen"

### Randfaelle
- **Duplikat-Treffer werden nicht geschrieben** — nur Meldezeile `übersprungen — ähnlich L{N}` bzw. `#{N}` (heute: vorgestrichen, „behalte" nimmt auf — die Veto-Moeglichkeit entfaellt mit der Rueckfrage)
  - **Geaendert bei der Umsetzung 2026-11-03 (Mismatch Schritt 1.2):** Duplikate werden gefragt, nicht nur gemeldet — ja/nein-Zeile im Kontrollpunkt (`ja` = nicht erfassen, `nein`/unklar = erfassen). Grund: Kopplungsregel „Meldeform folgt Vergleichsschaerfe" in `skills/CLAUDE.md`; der Vergleich ist unscharf, ein Falsch-Treffer ginge sonst still verloren
- **Mengengrenze bleibt:** mehr als 10 Funde → nichts automatisch schreiben, Rueckfall auf die Befehle im Report (Schutz gegen eine Fehlerkennung, die `lessons.md` auf einen Schlag fuellt)
- **Korrektur-Hinweis:** wurden Lektionen erfasst, traegt die Meldung `Falsch erfasst? → /dtb:lesson-curate` (bestehender Weg, append-only bleibt, Ausmusterung mit Grund)
- **Unveraendert:** Erfassungsquelle nicht installiert oder Struktur-Drift → Funde des Typs bleiben Befehle im Report (Rueckfall je Quelle); Schreibfehler mitten drin → melden, nie zurueckrollen
- Nur noch Zuordnungsfragen (frueher Teil B) offen → die Rueckfrage-Runde besteht nur aus diesen; sonst keine Runde (seit der Umsetzung 2026-11-03: Zuordnungs- und Duplikatfragen)

### Einschraenkungen
- **Keine Merge-Sperre wegen #177** (Entscheid 2026-11-03): Merge auch vor 2026-12-02 erlaubt. Die Nachmessung gilt dann fuer #177 und #173 gemeinsam (Checkpoint schneller + ohne Rueckfragen). Folgen:
  - die offene Aufgabe „Nachmessung #177" wird zur gemeinsamen Messung → in den Hand-off (zentrale `WORKFLOW_STATUS.md` gehoert nicht diesem Worktree)
  - die 3 Vergleichslaeufe von #177 pruefen zusaetzlich, ob die automatische Erfassung dieselben Funde schreibt, die bisher bestaetigt wurden
- **Regel und Skill aendern sich gemeinsam:** `DERIVED_STATE_RULES.md` §9 und die bewusste Kurzkopie im Checkpoint (Grep-Anker `Aufgaben-Abgaenge`). Bestandsprojekte bekommen das Verhalten per `kit-sync` mit dem Skill; ihre DSR-Kopie (Seed, nicht drift-geprueft) bleibt alt bis zum Neu-Ausrollen — akzeptiert
- **Checkpoint-Skill wird kuerzer, nicht laenger** (heute 829 Zeilen): Antwortregeln fuer Teil A und C entfallen
- Fachliche Constraints: keine

### Integrationspunkte
- **`dtb:no-loss-check` Abschlussfrage:** entfaellt heute beim Aufruf aus dem Checkpoint nur „mit nicht-leerer Vorlage" (dringende Gruppe ODER Ideen-Funde aus `## Kann warten`), weil dort die Sammelvorlage die eine Frage ist (#73). Ohne Teil A wuerde sie wieder auftauchen → **aus dem Checkpoint heraus nie mehr eine Abschlussfrage**; eigenstaendig aufgerufen unveraendert. Die Bedingung ist wortgleich auf beiden Seiten zu halten
- **Bestehende `· behalten`-Stempel** in alten Listen bleiben gueltig (juengeres Datum von `seit`/`behalten` zaehlt weiter), keine Bereinigung
- **Unveraendert:** `dtb:project-dashboard` (zaehlt ⏳ woertlich aus der Liste), Worktree-⏳ in `workflow-next`/`workflow-resume`/`backlog-status` (§10, anderer Mechanismus), Config-Key `status.alter_schwelle_tage` (bleibt fuer die ⏳-Markierung)
- Kopplungs-Hinweise „Kontrollpunkt Teil A" in `dtb:lesson`, `dtb:idea`, `dtb:idea-triage`, `dtb:no-loss-check` und die Zeile I in `skills/CLAUDE.md` nachziehen
- Externe Abhaengigkeiten: keine

---

## Abhaengigkeiten

- **`checkpoint-schneller` (#177, Fertig zum Testen, gemergt):** baut den `#### Kontrollpunkt` mit Teil A/B/C, den dieser Change auf die Zuordnungsfragen (Teil B) reduziert. Kein Konflikt — Merge-Sperre per Entscheid 2026-11-03 aufgehoben, Nachmessung bis 2026-12-02 wird gemeinsam

---

## Offene Punkte

- Wie oft kommen unsichere Zuordnungen bzw. Abgaenge ohne Beleg (frueher Teil B) tatsaechlich vor? Annahme „selten" ist ungezaehlt — z. B. mit `checkpoint-phasen.py` aus `checkpoint-schneller` an den Session-Logs pruefen
- Wie werden die Erfolgskriterien von #177 (Median ≤ 4 aktive min, 3 Vergleichslaeufe) fuer die gemeinsame Messung angepasst — und was ist das eigene Fertig-Kriterium von #173 (z. B. 0 Rueckfragen in Laeufen ohne unsichere Zuordnung)?
- Hand-off-Vormerkung: offene Aufgabe „Nachmessung #177" in `WORKFLOW_STATUS.md` zur gemeinsamen Messung #177 + #173 umbenennen (Orchestrator)

---

**Erstellt mit:** `/dtb:feature-discover`
