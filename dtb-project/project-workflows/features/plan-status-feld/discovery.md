# Discovery: plan-status-feld
<!-- resume: done -->

**Erstellt:** 2026-07-30
**Idee-Referenz:** Inbox #30 — plan.md-Kopf-Statusfeld (`Entwurf`/`Reviewed`) hat keinen schreibenden Pfleger, wird aber gelesen — Drift-Quelle gegen das Derived-State-Prinzip; zweiter Teilbefund: `workflow-next` Z. 53 ohne Checkbox-Guard
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| skills/dtb-impl-plan/SKILL.md | Z. 102: Template definiert das Kopf-Statusfeld — Entstehungsort; Wertemenge straffen |
| skills/dtb-workflow-next/SKILL.md | Z. 40 liest das Feld; Z. 53 einzige Pipeline-Zeile ohne Checkbox-Guard; Z. 115 Beispiel-Output |
| skills/dtb-workflow-status/SKILL.md | Z. 49–50 (Ableitung), Z. 85 (Gate „Plan-Review", liest nie gesetzten Wert `In Umsetzung`), Z. 138/174 |
| skills/dtb-backlog-status/SKILL.md | Z. 43: nennt das Feld, nicht unterscheidend — voraussichtlich kein Aenderungsbedarf |
| skills/dtb-plan-review/SKILL.md | Schreibt heute nichts — Traeger der Pfleger-Option (Feld am Review-Ende setzen) |
| skills/dtb-workflow-checkpoint/SKILL.md | Schritt 2 zaehlt Sync-Ziele abschliessend auf — Kandidat, falls Sync-Weg gewaehlt |
| skills/CLAUDE.md | Z. 54: dokumentiert die Feld-Konvention — nachziehen |
| dtb-project/project-rules/DERIVED_STATE_RULES.md | Kennt das Feld nicht (0 Treffer) — Kanonisierung als gepflegtes Anzeige-Feld |
| dtb-project/project-workflows/features/*/plan.md | Bestand (4 Koepfe): alle `Reviewed`, konsistent — Bestandspruefung faktisch erledigt |

Scan-Zusatzbefunde (2026-07-30): (1) `plan-review` und `workflow-checkpoint` haben 0 Treffer fuer
`Entwurf`/`Reviewed` — Nicht-Pfleger-Befund belegt. (2) Wertemenge im Template umfasst 4 Werte,
`In Umsetzung`/`Abgeschlossen` setzt niemand — `workflow-status` Z. 85 liest einen Wert, der nie
existieren kann. (3) Das Feld steht komplett ausserhalb des Ableitungs-Kanons der
`DERIVED_STATE_RULES.md`.

---

## Anforderungen

### Scope
**Enthalten:**
- Pfleger-Option: `dtb:plan-review` schreibt das Kopf-Statusfeld am Review-Ende selbst
  (`Entwurf` → `Reviewed`; Zusatz Datum/Verdikt nach gelebtem Bestandsmuster, z. B.
  „Reviewed (plan-review 2026-07-19: REVISE → 3 WARNs behoben)")
- Checkbox-Guard in `workflow-next` Z. 53: Zeile `Status Entwurf → Review ausstehend` greift nur
  bei 0/Y Checkboxen (analog Z. 54)
- Haertung `workflow-status`: Gate Z. 85 nicht laenger vom nie gesetzten Wert `In Umsetzung`
  abhaengig; Z. 49–50 konsistent nachziehen
- Wertemenge im impl-plan-Template (Z. 102) auf `Entwurf` / `Reviewed` straffen —
  Umsetzungsstand ist Sache von `## Progress` (Derived State), nicht des Kopffelds
- `DERIVED_STATE_RULES.md`: Feld als gepflegtes Anzeige-Feld mit benanntem Pfleger kanonisieren
- `skills/CLAUDE.md` Z. 54 an neue Wertemenge/Pfleger-Regel anpassen

**Nicht enthalten:**
- Bestandsmigration archivierter Plaene (`archive/*/plan.md`)
- Automatische Rueck-Stufung `Reviewed` → `Entwurf` bei Plan-Aenderungen nach dem Review
- Aenderungen an `backlog-status` (liest das Feld nicht unterscheidend)

### Gewuenschtes Verhalten
- **Still schreiben, im Report ausweisen (Punkt 1, Option A):** plan-review setzt das Feld am
  Review-Ende automatisch, ohne Bestaetigungsfrage; der Abschluss-Report weist die Aenderung als
  eine Zeile aus. Begruendung: 1 versionierte Zeile im eigenen Arbeitsbaum, trivial rueckholbar —
  eine Pflicht-Interaktion waere Reibung ohne Schutzwert und liesse das Feld erneut veralten
  (bewusster Kontrast zu commit-and-push `eda0ed1`, wo Aussenwirksamkeit die Bestaetigung verlangt)
- **Feld wird bei JEDEM Verdikt geschrieben (Punkt 2)** — Wert unterscheidet nach Startklarheit
  (`Reviewed` schaltet in workflow-next „Start ausstehend" frei, darf also nur bei startklarem Plan stehen):
  | Ausgang | Feld danach |
  |---------|-------------|
  | SOUND | `Reviewed (plan-review {Datum}: SOUND)` |
  | REVISE, Findings im selben Zug behoben | `Reviewed (plan-review {Datum}: REVISE → {N} WARNs behoben)` |
  | REVISE, Findings offen | `Entwurf (plan-review {Datum}: REVISE — Findings offen)` |
  | RETHINK | `Entwurf (plan-review {Datum}: RETHINK)` |
  Kerngedanke: Das Feld dokumentiert immer den LETZTEN Review-Stand — auch ein negatives Review
  hinterlaesst eine Spur, nichts veraltet mehr stumm
- **Leser melden Feld-Konflikte aktiv (Punkt 3, Option A):** Guard verhindert den Fehlvorschlag,
  ZUSAETZLICH ⚠-Konfliktzeile in workflow-next/workflow-status nach dem Derived-State-Muster
  („Artefakt gewinnt, melden — nicht selbst korrigieren"), z. B. „⚠ Kopf-Statusfeld sagt Entwurf,
  ## Progress zeigt 3/9 — Feld veraltet (plan-review nachtragen oder Feld korrigieren)"
- **UX-Muster uebernommen (Punkt 4, folgt aus 2+3):** ⚠-Konfliktzeilen-Format der read-side Skills
  (workflow-resume) + Vermerkformat des gelebten Bestands `Reviewed (plan-review {Datum}: {Verdikt})`

### Randfaelle
- **Feld fehlt komplett** (alter/handgeschriebener Plan): Leser behandeln es wie `Entwurf`
  (konservativster Schluss: kein Review-Nachweis), STILL — fehlende Info ist kein Konflikt,
  keine ⚠-Zeile. plan-review fuegt die Zeile beim Review-Ende an der Kopfposition ein
  (repariert die Luecke nebenbei)
- **Altwerte `In Umsetzung`/`Abgeschlossen`** (4-Werte-Template ist verteilt — Zielprojekte/Archiv):
  Leser werten sie STILL wie `Reviewed` (setzen logisch ein bestandenes Review voraus; Umsetzungsstand
  kommt ohnehin aus `## Progress`). **Unbekannte Werte** (Tippfehler/Freitext): wie fehlendes Feld
  (`Entwurf`-Semantik) + 1 Hinweiszeile „unbekannter Statuswert {X}". Selbstheilung: plan-review
  normalisiert beim naechsten Lauf automatisch (schreibt immer) — keine Bestandsmigration noetig
- **Feld ausserhalb der ersten 10 Zeilen:** Lesefenster = Definitionsfenster (wird in
  `DERIVED_STATE_RULES.md` kanonisiert). Eine `**Status:**`-Zeile ausserhalb ist KEIN Kopf-Statusfeld —
  weder gelesen noch von plan-review angefasst (kein Duplikat-Risiko bei zitierten Bloecken).
  Ausserhalb = fehlt → Randfall-1-Semantik; plan-review fuegt im Fenster ein (Kopfposition ~Z. 6)
- **REVISE-Findings erst NACH dem Lauf eingearbeitet** (Schritt 5 abgelehnt/vertagt):
  Normalweg = erneuter `/dtb:plan-review`-Lauf (prueft zugleich, ob die Einarbeitung die WARNs
  wirklich behebt — nur so bleibt „Reviewed" wahr). Manueller Flip bleibt als dokumentierte
  Ausnahme zulaessig, mit Vermerk-Pflicht: `Reviewed (manuell {Datum}: {Grund})` — gibt sich
  nicht als Review-Ergebnis aus

### Einschraenkungen
- **Distribution:** Geaenderte Skills sind Klasse A → normale kit-sync-Verteilung (beide Maschinen;
  andere Maschine steht auf `07d5107`, Sync-Paket waechst entsprechend)
- **Contracts unveraendert:** workflow-next/workflow-status bleiben read-only (⚠-Zeile ist
  Report-Output); plan-review schreibt via Schritt 5 bereits in plan.md — der Pfleger erweitert
  keinen Schreib-Contract
- **Derived-State-Kern unangetastet:** Feld bleibt reiner Review-Nachweis; „In Arbeit"-Ableitung
  laeuft unveraendert allein ueber `## Progress`
- **Seed-Skew bewusst hingenommen (entschieden 3d):** Die Kanonisierung landet in
  `DERIVED_STATE_RULES.md` (Klasse B, copied once) — Bestandsprojekte bekommen die neuen §-Regeln
  nicht automatisch, ihre global gesyncten Skills verhalten sich aber neu. Wird NICHT hier geloest,
  sondern als weiterer Beleg in INBOX #22 (Seed-Skew aktiv melden) eingezahlt. Schaden klein:
  die Leser-Regeln sind rueckwaertskompatibel tolerant (Randfaelle 1–3 funktionieren mit altem Seed)

### Integrationspunkte
- **Betroffene Skills/Dateien:** siehe `## Betroffene Module` (6 Skills + `DERIVED_STATE_RULES.md`
  + `skills/CLAUDE.md`); Verteilung ueber kit-sync (Klasse A); keine externen Abhaengigkeiten
- **Expliziter NICHT-Integrationspunkt (entschieden 3e):** `workflow-checkpoint` bleibt aussen vor —
  das Kopffeld wird NICHT in seine Sync-Ziele (Schritt 2) aufgenommen. Ein Feld, ein Pfleger
  (plan-review, Semantik „letzter Review-Stand"); ein zweiter Schreiber mit anderer Logik waere
  die naechste Drift-Quelle. Im Plan als Leitplanke vermerken: Sync-Ziel-Liste unveraendert lassen
- **INBOX #22:** bekommt bei der Umsetzung den Seed-Skew-Beleg aus 3d als Satz-Ergaenzung angehaengt

---

## Abhaengigkeiten

- Bestehende Features: 4 (`commit-and-push`, `fachfragen-erfassung`, `meeting-dump`,
  `open-question`) — alle „Fertig zum Testen", keines fasst workflow-next, workflow-status,
  plan-review oder impl-plan an → keine Konflikte
- `DERIVED_STATE_RULES.md` zuletzt von fachfragen-erfassung erweitert (§6, committed) —
  die Kanonisierung hier kommt als eigener § dazu, rein additiv
- Idee #23 (Multi-Repo-Begriff) wuerde spaeter ebenfalls `DERIVED_STATE_RULES.md` §2 anfassen —
  kein Artefakt vorhanden, kein Konflikt; §-Nummerierung sauber additiv halten

---

## Offene Punkte

- §-Verortung der Kanonisierung in `DERIVED_STATE_RULES.md`: eigener neuer § (analog §6) oder
  Unterabschnitt eines bestehenden §? — beim impl-plan entscheiden (Struktur der Regel-Datei sichten)

---

**Erstellt mit:** `/dtb:feature-discover`
