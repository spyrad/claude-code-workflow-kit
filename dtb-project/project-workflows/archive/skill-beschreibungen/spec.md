# Feature: Skill-Beschreibungen kürzen und abgrenzen

**Erstellt:** 2026-11-26
**Ziel:** Die Skill-Beschreibungen, die in jede Session geladen werden, sind kurz und klar voneinander abgegrenzt.
**Prioritaet:** Mittel
**Status:** Abgeschlossen <!-- abgeleitete Anzeige, wird von dtb:workflow-checkpoint synchronisiert (project-rules/DERIVED_STATE_RULES.md) -->

---

## Executive Summary

Die zehn vom Modell aufrufbaren Skills laden ihre Beschreibung in jede Session jedes Zielprojekts; vier davon sind länger als nötig (bis 1128 Zeichen), und vier Status-Skills überschneiden sich in ihren Auslösern, ohne sich gegenseitig auszuschließen. Der Change legt eine Längengrenze und eine Abgrenzungsform für Beschreibungen fest und bringt die betroffenen Skills darauf.

---

## Scope / Abgrenzung

### Enthalten
- Regel in der Skill-Konvention (`skills/CLAUDE.md`): Beschreibungen vom Modell aufrufbarer Skills höchstens 350 Zeichen; Form aus Auslöser-Phrasen, einem Satz Zweck und — bei Überschneidung — einem „Not for"-Satz; Details gehören in den Body
- Kürzen von `session-summary`, `idea-rank`, `no-loss-check` und `project-dashboard`
- Je ein „Not for"-Satz für `workflow-next`, `workflow-status`, `backlog-status` und `project-dashboard`

### Nicht enthalten
- Maschinelle Prüfung der Regel (Inbox #214)
- Längenprüfung im Gesundheits-Check des Kits
- Freigabe weiterer Skills für den Modellaufruf (Inbox #181 a)
- Gesperrte Skills — ihre Beschreibungen kosten keinen Session-Kontext

---

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Kürzen entfernt eine Auslöser-Phrase, der Skill wird seltener gewählt | Mittel | Mittel | Abgleich aller Auslöser-Phrasen vorher/nachher als Abnahmekriterium |
| Ein „Not for"-Satz verweist auf einen nicht existierenden Skill | Niedrig | Niedrig | Jeder Verweis wird gegen die vorhandenen Skills geprüft |
| Die Wirkung auf die Skill-Wahl ist im Worktree nicht prüfbar | Hoch | Niedrig | Auslöse-Probe nach Merge und Kit-Sync als offener Punkt |

---

## Dependencies

### Erforderlich vor Start
- [x] Messung der Ausgangslängen (erledigt in der Erhebung 2026-11-26)

### Referenz-Dokumente
- `skills/CLAUDE.md` - Form-Regel für das Frontmatter
- `features/skill-beschreibungen/discovery.md` - gemessene Längen und Fundstellen

---

## Success Criteria

**Das Feature gilt als erfolgreich wenn:**
- [ ] Alle zehn vom Modell aufrufbaren Skills haben eine Beschreibung von höchstens 350 Zeichen
- [ ] Die Regel (Länge, Form, „Not for"-Satz, Details in den Body) steht in `skills/CLAUDE.md`
- [ ] Jeder der vier Status-Skills schließt seine Nachbarn in einem „Not for"-Satz aus, mit Verweis auf existierende Skills
- [ ] Kein Auslöse-Anlass der gekürzten Skills ist verloren gegangen: jede weggefallene oder zusammengelegte Auslöser-Phrase ist aufgelistet und vom Menschen als abgedeckt bestätigt (wörtlicher Erhalt aller Phrasen passt bei `session-summary` nicht unter die Grenze — rund 320 Zeichen allein für die Phrasen)
- [ ] Alle zehn Beschreibungen beginnen mit `Use when:`

---

## Offene Punkte

- Auslöse-Probe nach Merge und Kit-Sync: In einer frischen Session die vier Status-Fragen stellen („was steht an", „wo steckt was", „offene Features", „Projektstand als Seite") und prüfen, ob der passende Skill gewählt wird

---

**Erstellt mit:** /dtb:feature-fast (Fast-Track, Sammelvorlage bestaetigt 2026-11-26)
