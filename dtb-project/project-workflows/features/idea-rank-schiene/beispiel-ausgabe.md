# Beispiel-Ausgabe: idea-rank-schiene

> Ablage fuer Schritt 1.1 (Manual-Gate der Ausgabeform) und 2.3 (Probelauf). Status-neutral.
> Datengrundlage: `INBOX.md` im Worktree `feature/idea-rank-schiene`, 20 Ideen mit Status `Offen`;
> `features/` enthaelt nur diesen Change, `BACKLOG.md` ohne aktive Zeilen.

## Beispiel 2026-10-29

Einstufung nach den Annahmen der Sammelvorlage: Dreier-Weiche aus `dtb:idea-review`, Worker nur bei
Schiene `Task`, Grundsatzfrage → Entscheidungsarbeit mit Default `Voll-Schiene`, `3+ Tage` nie
`Fast-Track`, Grenzfall → groessere Schiene.

```
# Ideen-Rangliste

**Stand:** 2026-10-29 · 20 offene Ideen bewertet

| # | Idee (kurz) | Aufwand | Schiene | Worker | Wichtigkeit | Bemerkung |
|---|---|---|---|---|---|---|
| 113 | Merkzettel nur ohne andere Liste | 0,5–1 Tag | Fast-Track | — | 🟠 mittel-hoch | Stichprobe ueber 16 Projekte am 2026-09-30 (ein Beleg), Statusdatei ueber 80 Zeilen; Vorbedingung fuer #173 (Vermutung) |
| 145 | Eingabe-Pruefung per Hook | 1–2 Tage | Voll-Schiene | — | 🟠 mittel-hoch | wiederkehrende Datenschutz-Fragen im PKP-Projekt (ein Beleg); neues Konzept (erster Hook im Kit); Sinnvoll erst nach #45 (Vermutung) |
| 164 | Zustaendigkeit und Pruefart kennzeichnen | 1–2 Tage + Discovery offen | Voll-Schiene | — | 🟠 mittel-hoch | Beispiele aus dem PKP-Projekt (ein Beleg); drei Teilthemen (Zustaendigkeit, technisch/fachlich pruefen, delegierte Arbeit) |
| 110 | Datenschutz-Schutz fuer Artefakt-Skills | 3+ Tage | Voll-Schiene | — | 🟠 mittel-hoch | Nutzerprojekt musste die Git-Historie umschreiben (ein Beleg); fuenf Skills plus Pre-Commit-Check, kit-weite Querwirkung |
| 112 | Checkliste vor `feature-start` | 2–4 h | Fast-Track | — | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; eine offene Entscheidung (Warnung oder Sperre) |
| 133 | Reife-Punktzahl fuer die Spec | 0,5–1 Tag + Discovery offen | Voll-Schiene | — | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; Ort, Kriterien und Schranken-Art offen |
| 173 | Checkpoint ohne Rueckfragen | 0,5–1 Tag | Fast-Track | — | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; beide Teile ausformuliert; Sinnvoll erst nach #113 (Vermutung) |
| 174 | `idea-rank` um Schiene erweitern | 0,5–1 Tag | Fast-Track | — | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; wird im Change idea-rank-schiene umgesetzt (Geplant) |
| 134 | Ablauf fuer Aenderungen mitten im Feature | 1–2 Tage + Discovery offen | Voll-Schiene | — | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; Traeger und Umfangs-Mass offen, Beruehrung mit `## Progress` |
| 98 | Autopilot fuer die Voll-Schiene | 3+ Tage | Voll-Schiene | — | 🟡 mittel | Transport belegt (2026-08-16/09-18), Antwortgeber-Muster fehlt; Vorbedingung fuer #143 (Vermutung); Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 111 | Neuplanungs-Schritt nach dem Merge | 2–4 h + Umsetzung offen | Voll-Schiene | — | 🟢 niedrig-mittel | Vorbild aus einem Kurs, kein Beleg; Traeger offen |
| 100 | Scan nach toten Teilen | 1–2 Tage + Discovery offen | Voll-Schiene | — | 🟢 niedrig-mittel | Aufraeumen; Traeger, Umfang und Vertrauensgrad offen |
| 171 | Zahlen in Tests maskieren | 1–2 Tage + Discovery offen | Voll-Schiene | — | 🟢 niedrig-mittel | Verlustschutz ohne eigenen Beleg; drei Fragen offen |
| 27 | `grill-me` gegen Greenfield abgrenzen | 1–2 h + Umsetzung offen | Voll-Schiene | — | 🟢 niedrig | ohne Bau entscheidbar (lesen, abgrenzen, entscheiden); Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 39 | Stitch als UI-Werkzeug pruefen | 1–2 h + Umsetzung offen | Voll-Schiene | — | 🟢 niedrig | Erkundung ohne konkreten Anlass |
| 99 | TypeSafe als Entscheidungs-Baustein | 1–2 h + Umsetzung offen | Voll-Schiene | — | 🟢 niedrig | keine eigene Station mehr, zieht in #98 ein; Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 138 | Claude-Code-Mods integrieren pruefen | 1–2 h + Umsetzung offen | Voll-Schiene | — | 🟢 niedrig | Erkundung ohne konkreten Anlass |
| 45 | Wo Hooks im Kit passen | 2–4 h + Umsetzung offen | Voll-Schiene | — | 🟢 niedrig | kein belegter Bedarf; Vorbedingung fuer #145 (Vermutung); Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 15 | Brownfield-Health-Check | 3+ Tage + Discovery offen | Voll-Schiene | — | 🟢 niedrig | Discovery 2026-07-28 abgebrochen, Vorstufe `stack-assess` fehlt; Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 143 | Autonome Teams in Wellen | 3+ Tage | Voll-Schiene | — | 🟢 niedrig | Inspiration ohne konkreten Anlass; Sinnvoll erst nach #98 (Vermutung) |

Momentaufnahme — INBOX.md unveraendert. Entscheidungen je Idee: /dtb:idea-review
```

Reihenfolge-Basis: #113, #145, #164, #110, #112, #133, #173, #174, #134, #98, #111, #100, #171, #27, #39, #99, #138, #45, #15, #143
Worker-Abdeckung: 0 Task-Ideen, davon 0 teilweise

### Beobachtungen fuer das Gate

1. **Worker-Spalte ist leer.** Kein einziger der 20 Eintraege landet auf der Schiene `Task` — die
   Worker-Spalte zeigt 20-mal `—` und wird an echten Daten nicht geprobt (Worker-Abdeckung 0).
2. **Grundsatzfragen auf der Voll-Schiene wirken schief.** Sechs Ideen (#27, #39, #45, #99, #111,
   #138) sind Grundsatzfragen mit 1–4 h Entscheidungsarbeit — nach der Default-Regel stehen sie auf
   `Voll-Schiene`, obwohl #27 ausdruecklich „ohne Bau entscheidbar" ist. Gegenvariante: Grundsatzfrage
   → `Task` (Entscheidung als einmaliger Handgriff). Dann haetten 6 Ideen ein Worker-Urteil — alle
   `nein`, weil eine Entscheidung ein menschliches Urteil ist (Worker-Kriterium 1).
3. **Breite:** sieben Spalten; die Bemerkung bleibt die breiteste Zelle, `Schiene`/`Worker` sind kurz.

### Gate-Entscheidungen 2026-10-29

**Grundsatzfrage → `Task`** (statt Default `Voll-Schiene`, Entscheidung des Nutzers am Gate 1.1).
Abweichung von Schritt 1.3 („Grundsatzfrage → Entscheidungsarbeit, Default `Voll-Schiene`") —
Mismatch-Option 1 (anpassen), umgesetzt in 1.3. Begruendung: die Entscheidungsarbeit einer
Grundsatzfrage ist ein einmaliger Handgriff ohne Spec (Dreier-Weiche „Operative Aufgabe").

Folge fuer das Beispiel — sechs Zeilen aendern sich, Reihenfolge unveraendert:

| # | Schiene | Worker | Grund Worker |
|---|---|---|---|
| 111 | Task | nein | Entscheidung = menschliches Urteil (Kriterium 1) |
| 27 | Task | nein | dto. |
| 39 | Task | nein | dto. |
| 99 | Task | nein | dto. |
| 138 | Task | nein | dto. |
| 45 | Task | nein | dto. |

Worker-Abdeckung (nach Entscheidung): 6 Task-Ideen, davon 0 teilweise — der Bemerkungs-Teil
`Worker: …` bleibt an echten Daten ungeprobt; die Probe in 2.3 braucht dafuer einen selbst
erzeugten Fall (L57).

Form-Entscheidung: eine Spalte — Kopf `| # | Idee (kurz) | Aufwand | Schiene | Wichtigkeit | Bemerkung |`; Zellwert `Fast-Track` / `Voll-Schiene` / `Task · Worker {ja/teilweise/nein}` (Rueckfall aus spec.md `## Offene Punkte`, Entscheidung des Nutzers am Gate 1.1, 2026-10-29)

## Probelauf 2026-10-29

Gegen die Repo-Fassung `skills/dtb-idea-rank/SKILL.md` (L74), Stand nach Phase 1 (`7e51cac`) plus
Wartungs-Hinweise aus 2.1; derselbe Inbox-Stand wie im Beispiel (20 `Offen`-Ideen, Worktree
unveraendert).

### (a) Rangliste nach dem neuen Regeltext

Struktur-Check (Schritt 3a): installierte Kopien und Repo-Fassung tragen je genau einen Anker
(`grep -cF` = 1 fuer Dreier-Weiche und Worker-Raster) → keine ⚠-Zeile.

```
# Ideen-Rangliste

**Stand:** 2026-10-29 · 20 offene Ideen bewertet

| # | Idee (kurz) | Aufwand | Schiene | Wichtigkeit | Bemerkung |
|---|---|---|---|---|---|
| 113 | Merkzettel nur ohne andere Liste | 0,5–1 Tag | Fast-Track | 🟠 mittel-hoch | Stichprobe ueber 16 Projekte am 2026-09-30 (ein Beleg), Statusdatei ueber 80 Zeilen; Vorbedingung fuer #173 (Vermutung) |
| 145 | Eingabe-Pruefung per Hook | 1–2 Tage | Voll-Schiene | 🟠 mittel-hoch | wiederkehrende Datenschutz-Fragen im PKP-Projekt (ein Beleg); neues Konzept (erster Hook im Kit); Sinnvoll erst nach #45 (Vermutung) |
| 164 | Zustaendigkeit und Pruefart kennzeichnen | 1–2 Tage + Discovery offen | Voll-Schiene | 🟠 mittel-hoch | Beispiele aus dem PKP-Projekt (ein Beleg); drei Teilthemen (Zustaendigkeit, technisch/fachlich pruefen, delegierte Arbeit) |
| 110 | Datenschutz-Schutz fuer Artefakt-Skills | 3+ Tage | Voll-Schiene | 🟠 mittel-hoch | Nutzerprojekt musste die Git-Historie umschreiben (ein Beleg); fuenf Skills plus Pre-Commit-Check, kit-weite Querwirkung |
| 112 | Checkliste vor `feature-start` | 2–4 h | Fast-Track | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; eine offene Entscheidung (Warnung oder Sperre) |
| 133 | Reife-Punktzahl fuer die Spec | 0,5–1 Tag + Discovery offen | Voll-Schiene | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; Ort, Kriterien und Schranken-Art offen |
| 173 | Checkpoint ohne Rueckfragen | 0,5–1 Tag | Fast-Track | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; beide Teile ausformuliert; Sinnvoll erst nach #113 (Vermutung) |
| 174 | `idea-rank` um Schiene erweitern | 0,5–1 Tag | Fast-Track | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; wird im Change idea-rank-schiene umgesetzt (In Arbeit) |
| 134 | Ablauf fuer Aenderungen mitten im Feature | 1–2 Tage + Discovery offen | Voll-Schiene | 🟡 mittel | regelmaessig genutzter Ablauf, kein Beleg; Traeger und Umfangs-Mass offen, Beruehrung mit `## Progress` |
| 98 | Autopilot fuer die Voll-Schiene | 3+ Tage | Voll-Schiene | 🟡 mittel | Transport belegt (2026-08-16/09-18), Antwortgeber-Muster fehlt; Vorbedingung fuer #143 (Vermutung); Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 111 | Neuplanungs-Schritt nach dem Merge | 2–4 h + Umsetzung offen | Task · Worker nein | 🟢 niedrig-mittel | Vorbild aus einem Kurs, kein Beleg; Traeger offen |
| 100 | Scan nach toten Teilen | 1–2 Tage + Discovery offen | Voll-Schiene | 🟢 niedrig-mittel | Aufraeumen; Traeger, Umfang und Vertrauensgrad offen |
| 171 | Zahlen in Tests maskieren | 1–2 Tage + Discovery offen | Voll-Schiene | 🟢 niedrig-mittel | Verlustschutz ohne eigenen Beleg; drei Fragen offen |
| 27 | `grill-me` gegen Greenfield abgrenzen | 1–2 h + Umsetzung offen | Task · Worker nein | 🟢 niedrig | ohne Bau entscheidbar (lesen, abgrenzen, entscheiden); Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 39 | Stitch als UI-Werkzeug pruefen | 1–2 h + Umsetzung offen | Task · Worker nein | 🟢 niedrig | Erkundung ohne konkreten Anlass |
| 99 | TypeSafe als Entscheidungs-Baustein | 1–2 h + Umsetzung offen | Task · Worker nein | 🟢 niedrig | keine eigene Station mehr, zieht in #98 ein; Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 138 | Claude-Code-Mods integrieren pruefen | 1–2 h + Umsetzung offen | Task · Worker nein | 🟢 niedrig | Erkundung ohne konkreten Anlass |
| 45 | Wo Hooks im Kit passen | 2–4 h + Umsetzung offen | Task · Worker nein | 🟢 niedrig | kein belegter Bedarf; Vorbedingung fuer #145 (Vermutung); Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 15 | Brownfield-Health-Check | 3+ Tage + Discovery offen | Voll-Schiene | 🟢 niedrig | Discovery 2026-07-28 abgebrochen, Vorstufe `stack-assess` fehlt; Verweis ausserhalb der Inbox — Reihenfolge nicht pruefbar |
| 143 | Autonome Teams in Wellen | 3+ Tage | Voll-Schiene | 🟢 niedrig | Inspiration ohne konkreten Anlass; Sinnvoll erst nach #98 (Vermutung) |

Momentaufnahme — INBOX.md unveraendert. Entscheidungen je Idee: /dtb:idea-review
```

Regel-Abdeckung: Regel 1 (Grundsatzfrage → `Task`) 6×, Regel 2 (`3+ Tage` → nie Fast-Track) 4×
(#110, #98, #15, #143), Fast-Track nach Weiche 4× (#113, #112, #173, #174), Worker-Zusatz 6× `nein`.

### (b) Reihenfolge-Vergleich

Probelauf: #113, #145, #164, #110, #112, #133, #173, #174, #134, #98, #111, #100, #171, #27, #39, #99, #138, #45, #15, #143
Basis (1.1): identisch — 20/20 Positionen gleich. Die Schiene verschiebt keine Zeile (4.5).

### (c) Schreibtisch-Probe der Fehlerpfade

Die Aufloesung bevorzugt die installierte Kopie; deshalb wurden die Quellpfade fuer die Probe
ausdruecklich auf selbst erzeugte Objekte im Scratchpad umgelenkt (L57). Installierte Kopien unter
`~/.claude/` blieben unberuehrt (L54).

| Pfad | Probe-Objekt | Befund des Checks | Erwartete Ausgabe nach Schritt 3a | Ergebnis |
|------|--------------|-------------------|-----------------------------------|----------|
| (i) Installation | Worker-Quelle: `probe/global/…` und `probe/projekt/…`, beide nicht angelegt | beide Aufloesungen leer (`fehlt` / `fehlt`) | `⚠ Regelquelle dtb-worker weder global (~/.claude/skills/) noch im Projekt gefunden — Einstufung als „?" → /dtb:kit-sync sync`; Task-Zeilen `Task · Worker ?`, Fast-Track/Voll-Schiene unveraendert | wie erwartet — Fall 1, nicht Fall 2 |
| (ii) Drift | Weiche: `probe/drift/dtb-idea-review/SKILL.md`, Kopie ohne Fett-Zeile (211 Zeilen, Anker 0) | Datei vorhanden, `grep -cF` = 0 | `⚠ Struktur-Check: dtb-idea-review/SKILL.md — Anker „**Ausarbeiten (2) — Dreier-Weiche (Groesseneinschaetzung):**" nicht gefunden; Einstufung als „?" → dtb:idea-rank an die neue Struktur anpassen`; alle 20 Schiene-Zellen `?`, Rangliste sonst vollstaendig | wie erwartet — Fall 2, nicht Fall 1 |

Grenze der Probe: Sie belegt die Fallunterscheidung (vorhanden/leer, Anker ja/nein) an echten
Grep-Befunden; dass ein Modelllauf daraus genau die Zeilen formuliert, zeigt erst ein Lauf mit
fehlender bzw. gedrifteter installierter Kopie.

### (d) Zusatzfall `teilweise` (selbst erzeugt, L57)

Kein echter Eintrag erreicht `teilweise` (Worker-Abdeckung 6/0). Selbst erzeugter Fall: „#900 —
Tippfehler in `README.md` korrigieren, betroffene Stelle noch nennen" → Weiche: Operative Aufgabe →
`Task`; Raster: Kriterium 1 ja (Grep), 2 nein (Stelle offen — mit einer kurzen Antwort schliessbar),
3 ja, 4 ja → `teilweise`. Zelle `Task · Worker teilweise`, Bemerkung Teil 3:
`Worker: Scope nicht geschlossen (Stelle nennen)` — Position nach dem Grund der Wichtigkeit, vor
der Reihenfolge, wie in Schritt 5 festgelegt.
