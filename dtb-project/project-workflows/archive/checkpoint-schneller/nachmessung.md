# Nachmessung: Checkpoint schneller + Checkpoint ohne Rueckfragen

**Datum:** 2026-11-20
**Gilt fuer:** #177 `checkpoint-schneller` und #173 `checkpoint-ohne-rueckfragen` (gemeinsame Nachmessung, Entscheid 2026-11-03)
**Werkzeug:** `checkpoint-phasen.py` (dieser Ordner), Segmente gefiltert auf Start nach dem Merge + kit-sync von #173
(2026-11-03 17:35); Vorher-Wert: Segmente 2026-10-05 .. Merge #177 (2026-11-02 13:10)
**Quelle:** Claude-Code-Protokolle dieses Rechners, alle Projekte (`~/.claude/projects`); der zweite Rechner ist nicht enthalten

> Status-neutral: Beleg fuer die Success Criteria beider Specs und die Abnahme, keine Statusquelle
> (`DERIVED_STATE_RULES.md` §1.1). Nur Zahlen und Kategorien — keine Auszuege aus fremden Sitzungen (L109).

## Ergebnis

| Groesse | Vorher | Nachher | Kriterium |
|---------|--------|---------|-----------|
| Ausgewertete Laeufe (normal + handoff mit Kern) | 58 | 58 | ≥ 10 ✅ |
| Kern-Median (aktive min) | 5,2 | **3,0** | ≤ 4 ✅ |
| Segment-Median (aktive min) | 6,9 | 4,6 | — |
| Antworten „Alters-Vorlage" | 10 (22,9 min) | **0** | = 0 ✅ |
| Antworten „Sammelvorlage/Kontrollpunkt" | 38 (55,8 min) | 2, beide Duplikatfragen (Lektion 2026-11-17, Idee 2026-11-19) | nur Zuordnung/Duplikat ✅ |
| Commit-Frage durch den Checkpoint | ja | keine — Commit-Antworten nur nach Hinweis „uncommittet" oder auf Nachfrage des Menschen | ✅ |

## Vergleichslaeufe (#177: Verlustpruefung unveraendert, Funde landen)

- `skills/dtb-no-loss-check/` seit dem Merge von #173 (2026-11-03) unveraendert (`git log`)
- Drei echte Laeufe in diesem Repo, laut Session-Log gemeldete Funde gegen die Zieldateien geprueft — alle vorhanden:
  - 2026-11-06: L119–L124 in `lessons.md`, #189–#191 im Becken
  - 2026-11-09: L125–L127 in `lessons.md`, #192 im Becken
  - 2026-11-12: L135–L137 in `lessons.md`, #207 im Becken
- Ein Vorher-Nachher-Lauf am selben Gespraech war nachtraeglich nicht mehr moeglich; dieser Beleg ersetzt ihn

## Grenzen und Befunde

- **Mess-Skript:** Die Kategorie „Sammelvorlage/Kontrollpunkt" erkennt den Text des neuen Kontrollpunkts nicht
  mehr (Muster `Kontrollpunkt —`); die Antworten fallen in „sonstiges" (47 nachher, davon die meisten
  Folgearbeit im selben Segment) und wurden von Hand zugeordnet
- **Stopp nach der Verlustpruefung:** in 4 von 58 Laeufen (alle PKP) blieb der Checkpoint nach dem Bericht
  der Verlustpruefung stehen, der Mensch musste anstossen — keine Frage, aber eine Wartestelle → Befund #211
