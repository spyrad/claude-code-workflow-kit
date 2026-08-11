# Workflow-Status: claude-code-workflow-kit

**Letztes Update:** 2026-08-10
**Letzter Session-Log:** `dtb-project/project-changelog/2026-08/2026-08-10.md`

---

## Status (generiert aus Artefakten — nicht manuell editieren)

| Item | Status (abgeleitet) | Fortschritt | Naechster Schritt |
|------|---------------------|-------------|-------------------|
| feature-fast (#37) | Fertig zum Testen | 11/11 | Restabnahme: 2 UX-Urteile + Lauf mit gefixter Fassung (`1eec2ea`) |
| output-style-gezielt (#40) | Fertig zum Testen | 11/11 | Im Alltag beobachten, dann Abnahme im Checkpoint |
| feature-start-statusfeld (#50) | Fertig zum Testen | 5/5 | Verhaltenstests gegen die gefixte Fassung, dann Abnahme |
| meeting-agenda (#25) | Fertig zum Testen | 5/5 | Restabnahme dreigeteilt — Positiv-Lauf nur ausserhalb des Kits moeglich |

Anzeigefelder synchron zur Ableitung. Keine Feld-Konflikte.
⚠ feature-fast · meeting-agenda · feature-start-statusfeld: `review.md` sagt je „REJECTED", die Triage-Bilanzen zeigen alle Findings behoben — eingefrorene Verdikt-Felder, drei #35-Belege.

---

## Kontext (manuell)

| Kennzahl | Wert |
|----------|------|
| **Blocker** | Keine |
| **Erreicht (2026-08-10)** | Maschinen-Nachlauf auf dem zweiten Rechner abgeschlossen: `gitattributes-eol` **6/6 und archiviert** (`git status` leer bei 196x `i/lf` trotz `core.autocrlf=true` — der Nachweis, den kein Clone-Test liefern konnte), Sicherungs-Branch geloescht, `autonome-schiene` archiviert. Erstmals seit 2026-08-05 **kein Item „In Arbeit"** |
| **Kernbefund** | `lessons.md` endet auf **dieser** Maschine bei L14 — L15-L21 (u.a. L18/L20/L21) sind nie angekommen, weil die Datei ungetrackt ist (#34). Die vier Prior-Leser laufen hier mit drei Wochen altem Stand; die heutige Verlustpruefung konnte nur gegen L1-L14 abgleichen. Erster konkreter Schadensbeleg → **#64** |
| **Kit-Stand (maschinenlokal!)** | Lock **46 Artefakte @ `f0c204a`** auf diesem Rechner (vorher 44 @ `3d15d0a`, 10 eingespielt). Die Kennzahl gilt **nicht** projektweit — siehe #66 |
| **Notizen** | Lektionen L1-L14 + **L22, L23** (ungetrackt, #34 — Luecke L15-L21 bewusst stehen gelassen). Ideen-Bestand **34 offen**. ROADMAP-§5-Sync zum **neunten** Mal leer. Verlustpruefung 2026-08-10: 5 Funde, **alle 5 abgesetzt** |

---

## Offene Aufgaben

- [ ] **L20-Bestandsnachlauf** — `feature-start-statusfeld/plan.md:101` + `meeting-agenda/plan.md:104` gegen die Pruefragefrage durchgehen; zahlt auf zwei der vier Restabnahmen ein
- [ ] **L22 + L23 nach `skills/CLAUDE.md` heben** — beide `Applies-to: alle`, beide Kit-Konventionen; auf `lessons.md` allein gelten sie nur hier (#64)
- [ ] **9 Funde aelterer Verlustpruefungen absetzen** — 4 vom 2026-08-07 S1 + 5 vom 2026-08-06
- [ ] L11-L14 + L22/L23 nach `skills/CLAUDE.md` heben (lessons.md ungetrackt — #34)
- [ ] #66 · #65 · #64 · #63 · #62 · #59 · #58 · #57 · #56 · #55 · #54 · #53 · #52 · #51 · #35 · #33 entscheiden
- [ ] Restabnahmen `feature-fast` · `meeting-agenda` · `output-style-gezielt` · `feature-start-statusfeld`
- [ ] Config-Platzhalter fuellen · ROADMAP-Vorlage fuellen oder entfernen (9x leer) · pkp intern committen (`UI.md` + Tokens)

---

## Abgeschlossene Meilensteine (kompakt)

| Datum | Meilenstein | Ergebnis | Details |
|-------|-------------|----------|---------|
| 2026-08-10 | Maschinen-Nachlauf + Archiv-Lauf | `gitattributes-eol` 6/6, kit-sync 44→46 (zwei Laeufe, L22), 2 Ordner archiviert, 5 Verlustfunde abgesetzt | `2026-08/2026-08-10.md` |
| 2026-08-09 | `autonome-schiene` abgenommen + Archiv-Lauf | 4/4 Manual-Kriterien belegt; 3.3-Protokoll nachgeholt (nie abgelegt gewesen); `edca1e0`, `c56abff` | `2026-08/2026-08-09.md` (S2) |
| 2026-08-09 | Autonome Lane erstmals komplett durchlaufen (`pipeline-kanten-reziprok`) | Worker gruen nach 1 Versuch (7 Min), `a79c218` gepusht; zwei Befunde ueber die Lane (L18, #58) | `2026-08/2026-08-09.md` (S1) |

---

## Pausierte Themen

### Idee #15: `10x-health-check`-Pendant
**Status:** Bewusst vertagt (2026-07-28) — Ast-Entscheidung (Brownfield-Zweig), braucht Fokus.
**Details:** `INBOX.md` #15; Analysen `2026-07/2026-07-27.md`, `2026-07/2026-07-28.md`

---

## Handoff

**Naechster Befehl:** `/dtb:commit-and-push` — 11 uncommittete Pfade: 6 Umbenennungen aus dem
Archiv-Lauf (2 Ordner), 4 geaenderte Workflow-Dateien, 1 neuer Session-Log. Nichts davon ist
gepusht; die Arbeit dieser Sitzung existiert nur lokal (`lessons.md` bleibt ungetrackt — #34).
**Empfehlung:** Neue Session mit `/clear` starten, dann `/dtb:workflow-resume`, danach obigen
Befehl. **Gueltigkeitsbedingung:** gilt, solange `git status --short` im Kit-Repo nicht leer
ist. Ist bereits committet und gepusht, ist der naechste Schritt der **L20-Bestandsnachlauf**
(`feature-start-statusfeld/plan.md:101`, `meeting-agenda/plan.md:104`) — er geht den vier
Restabnahmen voraus, weil zwei davon an genau diesen Stellen haengen.
⚠ **Ableitung bewusst uebersteuert:** Die Regel zeigt bei `review.md` mit REJECTED auf
`/dtb:implement` — bei den drei betroffenen Features sind die Findings behoben bzw. bewusst
verworfen (Triage-Bilanzen in den Session-Logs). Eingefrorene Verdikt-Felder, #35-Belege.
