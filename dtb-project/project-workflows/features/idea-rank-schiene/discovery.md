# Discovery: idea-rank-schiene
<!-- resume: done -->

**Erstellt:** 2026-10-29
**Idee-Referenz:** Inbox #174 — "`dtb:idea-rank` um die Einstufung der Schiene erweitern. Die Rangliste soll je Idee zusätzlich zeigen, welche Art von Arbeit es ist: Voll-Schiene oder Task, schnelle kleine Aufgabe oder größer — eingestuft nach allen Klassen, die das Kit bisher kennt (z. B. die Dreier-Weiche aus `dtb:idea-review`: Task `/dtb:task`, Fast-Track `/dtb:feature-fast`, Voll-Schiene `/dtb:feature-discover`; ggf. auch die Worker-Tauglichkeit aus `dtb:worker`)."
**Status:** Abgeschlossen

---

## Betroffene Module

| Pfad | Beschreibung |
|------|-------------|
| `skills/dtb-idea-rank/SKILL.md` | Kern: Struktur-Check auf die zwei Regelquellen, Einstufungsregeln (Schiene, Worker), zwei neue Tabellenspalten, Bemerkungs-Teil fuer `teilweise`, description |
| `skills/dtb-idea-review/SKILL.md` | Wartungs-Hinweis (Struktur-Anker) an der Dreier-Weiche (`**Ausarbeiten (2) — Dreier-Weiche (Groesseneinschaetzung):**`, Zeile 144) |
| `skills/dtb-worker/SKILL.md` | Wartungs-Hinweis (Struktur-Anker) am Raster (`### Schritt 2: Urteil je Eintrag (Bewertungsraster: Worker-Tauglichkeit)`, Zeile 69); der Schwester-Raster-Hinweis in Zeile 71 sieht das Andocken bereits vor |
| `CLAUDE.md` | Kit-Doku: Beschreibung von `idea-rank` unter „Idea management" (Zeile 51) |
| `README.md` | Kit-Doku: Skill-Tabelle, Zeile `/dtb:idea-rank` (Zeile 72) |

---

## Anforderungen

### Scope
**Enthalten:**
- Je Idee der Rangliste genau ein **Schienen-Wert** nach der Dreier-Weiche aus `dtb:idea-review`: `Task` (`/dtb:task`), `Fast-Track` (`/dtb:feature-fast`), `Voll-Schiene` (`/dtb:feature-discover`)
- Je Idee genau ein **Worker-Wert** nach den vier Kriterien aus `dtb:worker` (`ja` / `teilweise` / `nein`) — nur bei Schiene `Task`, sonst `—`
- Kopplung **per Referenz**: idea-rank liest beide Regelstellen zur Laufzeit (installierte Kopie unter `~/.claude/skills/`, Fallback `skills/` im Projekt-Root) und prueft vorher beide Anker (Struktur-Check)
- Wartungs-Hinweise an beiden Quell-Ankern, Nachzug der Kit-Doku

**Nicht enthalten:**
- Aenderung der Dreier-Weiche oder des Worker-Rasters selbst (Heuristik und Kriterien bleiben, wie sie sind)
- Aenderung der Sortierung (4.4) oder der Wichtigkeits-/Aufwand-Stufen
- Uebernahme der Einstufung durch `dtb:idea-review` — der Review schaetzt weiterhin selbst ein (wie bei der Reihenfolge: die Rangliste ordnet, der Review entscheidet)
- Freigabe oder Start von Workern aus der Rangliste heraus

### Gewuenschtes Verhalten
- Die Tabelle traegt zwei zusaetzliche Spalten `Schiene` und `Worker` zwischen `Aufwand` und `Wichtigkeit`
- `Worker: teilweise` nennt die eine Luecke als eigenen Bemerkungs-Teil `Worker: {fehlendes Kriterium}`; `ja`/`nein` ohne Text
- Grenzfall zwischen zwei Schienen → die groessere; Grenzfall beim Worker → das schwaechere Urteil (gleiche Vorsicht wie bei Wichtigkeit/Aufwand)
- Konsistenz mit dem Aufwand: eine Idee mit Aufwand `3+ Tage` (mehrere Phasen) ist nie `Fast-Track`, weil der Fast-Track auf max. 2 Plan-Phasen begrenzt ist
- Schiene und Worker aendern die Zeilen-Reihenfolge nicht
- Die Sicht bleibt rein lesend und ohne Rueckfragen

### Randfaelle
- **Grundsatzfrage** (Aufwand mit Zusatz `+ Umsetzung offen`): die Schiene bezieht sich auf die Entscheidungsarbeit, Default `Voll-Schiene` (bei Unsicherheit der sichere Default der Dreier-Weiche)
- **Quell-Skill fehlt** (weder installiert noch im Projekt) → Installations-Pfad: betroffene Spalte zeigt `?`, eine ⚠-Zeile mit Verweis auf `/dtb:kit-sync`
- **Quell-Skill vorhanden, Anker fehlt** → Drift-Pfad: betroffene Spalte zeigt `?`, eine ⚠-Zeile; die beiden Pfade werden nie vermischt
- **Teil-Routing (`(Rest)`)**: Schiene und Worker bewerten nur den ungerouteten Rest (wie Aufwand und Wichtigkeit)
- **Abweichung zur Worker-Sicht**: `dtb:worker` bewertet alle offenen Ideen; eine Idee mit Schiene `Fast-Track`/`Voll-Schiene` zeigt hier `—`, auch wenn die Worker-Sicht sie anders einstuft — bewusste Abgrenzung, weil sie vor einem Worker-Lauf Spec und Plan braeuchte

### Einschraenkungen
- `allowed-tools` bleibt `Read, Glob, Grep` (genuegt fuer Struktur-Check und Lesen der Quellen)
- Die Regeln der Quellen werden nicht kopiert — sonst entsteht eine dritte Fassung der Dreier-Weiche bzw. eine zweite des Worker-Rasters
- `INBOX-BEFUNDE.md` bleibt ungelesen (§6.4)

### Integrationspunkte
- `dtb:idea-review` (Dreier-Weiche) und `dtb:worker` (Raster) als Regelquellen per Struktur-Check — Muster wie `dtb:feature-fast` Schritt 2 und `dtb:pane-start`
- `dtb:kit-sync` als Redirect im Installations-Pfad

---

## Abhaengigkeiten

- Keine laufenden Changes unter `features/` (Ordner war vor diesem Change leer)
- Vorgaenger-Change `archive/idea-rank/` (abgeschlossen) — Tabellen-Form seit 2026-09-17 ist die Basis

---

## Offene Punkte

- Sind sieben Spalten im Chat noch lesbar? Wird an der Beispiel-Ausgabe mit echten Daten entschieden (Manual-Gate Phase 1); Rueckfall: `Schiene` und `Worker` in eine Spalte zusammenlegen (z.B. `Task · Worker ja`)

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-10-29)
