# DTB Session Recovery

Rette eine festgefahrene Development-Session durch strukturierte Analyse und Clean-Start-Zusammenfassung.

## Wann verwenden?

Nutze diesen Command wenn:
- Die Session sich im Kreis dreht
- Mehr Probleme entstehen als gelöst werden
- Du neu starten willst, aber Learnings bewahren möchtest
- Nach 1-2 Stunden ohne Fortschritt

## Aufgabe

Analysiere die aktuelle Konversation objektiv und extrahiere actionable Insights für einen Neustart.

## Analyse-Prozess

Analysiere die Konversations-History oben und erstelle eine detaillierte, objektive Zusammenfassung.
Fokussiere auf **Spezifika, nicht Generalisierungen**.

## Output-Format

Erstelle die Analyse in diesem Format:

```markdown
# Session Recovery: {KURZBESCHREIBUNG}
**Datum:** {DD.MM.YYYY} | **Zeit:** {HH:MM}
**Session Start:** {ca. Zeit} | **Stuck Point:** {ca. Zeit}

---

## ✅ Was funktioniert und behalten werden sollte

### Element 1: {Beschreibung}
- **Implementation**: `{datei/funktion}`
- **Warum es funktioniert**: {Anforderung die erfüllt wird}
- **Behalten weil**: {Begründung}
- **Code**:
```{language}
{relevanter Code-Schnipsel}
```

### Element 2: {Beschreibung}
...

---

## ❌ Wo unser Ansatz gescheitert ist

### Entscheidungspunkt 1: {Beschreibung}

**Was wir getan haben**:
{Spezifische Entscheidung mit Code/Config}

**Erwartetes Verhalten**:
{Was sollte passieren - konkret}

**Tatsächliches Verhalten**:
{Was tatsächlich passiert - konkret}

**Spezifische Fehler**:
```
{Fehlermeldungen oder konkrete Symptome}
```

**Root Cause**:
{Warum ist es schiefgegangen?}

---

### Entscheidungspunkt 2: {Beschreibung}
...

---

## 💡 Was wir gelernt haben

### Neue Informationen entdeckt
1. **{Discovery 1}**
   - Quelle: {Wo haben wir das herausgefunden?}
   - Impact: {Wie ändert das unseren Ansatz?}

2. **{Discovery 2}**
   ...

### Ursprüngliche Annahmen die falsch waren
| Annahme | Realität | Impact |
|---------|----------|--------|
| {Was wir dachten} | {Was tatsächlich ist} | {Konsequenz} |

### Zusätzliche Anforderungen/Limitierungen
- **{Requirement}**: {Beschreibung - nicht initial berücksichtigt}

---

## 🎯 Aktualisierter Problem-Kontext

> Vollständige Problem-Beschreibung für neue Konversation.
> Detailliert genug, dass ein unabhängiger Entwickler das Problem ohne Zugriff auf diese Konversation verstehen kann.

### Ziel
{Was wir erreichen wollen - präzise}

### Aktueller Status

**Was existiert:**
- `{datei}`: {Status/Funktionalität}
- `{config}`: {Aktueller Wert}

**Was funktioniert:**
- {Feature/Funktion}: {Wie es funktioniert}

**Was NICHT funktioniert:**
- {Problem}: {Konkrete Symptome}

### Constraints

**Technische Limitierungen:**
- {Limitation 1}: {Beschreibung}

**Architektur-Vorgaben:**
- {Vorgabe}: {Warum wichtig}

**Performance-Anforderungen:**
- {Anforderung}: {Zielwert}

### Reproduktions-Schritte

Wie man das Problem nachstellen kann:
```bash
# Schritt 1
{command oder action}

# Schritt 2
{command oder action}

# Erwartetes Ergebnis
{was sollte passieren}

# Tatsächliches Ergebnis
{was passiert}
```

---

## 🚀 Empfohlene Nächste Schritte

### Ansatz für Neustart

**Option 1: {Beschreibung}** ⭐ (Empfohlen)
- **Vorteil**: {Warum besser}
- **Nachteil**: {Trade-offs}
- **Schritte**:
  1. {Konkreter Schritt}
  2. {Konkreter Schritt}

**Option 2: {Beschreibung}**
- **Vorteil**: {Warum in Betracht ziehen}
- **Nachteil**: {Trade-offs}

### Was NICHT nochmal versuchen
- ❌ {Ansatz}: {Warum es nicht funktioniert hat}

### Quick Wins (falls möglich)
- [ ] {Kleine Änderung die sofort hilft}

---

## 📁 Betroffene Dateien & Konfiguration

### Zu überprüfen
- `{datei}`: {Was checken}
- `{config}`: {Welche Werte}

### Zu ändern (wahrscheinlich)
- `{datei}`: {Vermutete Änderung}

### Nicht anfassen
- `{datei}`: {Warum nicht ändern}

---

## 🔍 Debug-Informationen für Neustart

### Relevante Log-Ausgaben
```
{Wichtige Logs die das Problem zeigen}
```

### Environment
- OS: {Betriebssystem}
- Version: {Relevante Versionen}
- Dependencies: {Wichtige Package-Versionen}

### Reproduzierbarkeit
- [ ] Passiert immer
- [ ] Passiert manchmal ({Muster})
- [ ] Nur unter bestimmten Bedingungen: {Bedingungen}

---

## 💭 Offene Fragen für Neustart

1. **{Frage 1}**
   - Warum wichtig: {Kontext}
   - Mögliche Antworten: {Optionen}

2. **{Frage 2}**
   ...

---

## 📊 Session-Statistik

- **Dauer bis Stuck**: ~{X} Minuten/Stunden
- **Anzahl Lösungsversuche**: ~{N}
- **Code-Änderungen**: ~{N} Dateien
- **Hauptproblem**: {Kategorie: Architecture / Bug / Config / Misunderstanding}

---

## ✨ Positive Erkenntnisse

Was hat gut funktioniert (für zukünftige Sessions):
- {Approach/Tool/Method}: {Warum gut}

---

## 🎯 Action Plan für Clean Start

### Sofort (vor Neustart)
- [ ] {Aktion}: {Warum}
- [ ] Diese Recovery-Datei als Referenz nutzen

### Im Neustart (erste Schritte)
1. {Schritt 1}
2. {Schritt 2}
3. {Schritt 3}

### Validierung
- [ ] {Check 1}: {Wie testen}
- [ ] {Check 2}: {Wie testen}
```

## Speicherung

Speichere die Recovery-Analyse mit dem Write Tool:
- Pfad: `docs/recovery/YYYY-MM-DD-HH-MM-{kurzbeschreibung}.md`
- Falls `docs/recovery/` nicht existiert, erstelle es

## Richtlinien

- **Spezifisch, nicht generell**: "Code funktioniert nicht" → Beschreibe exaktes Verhalten
- **Fakten, nicht Schuld**: Objektive Analyse, kein Blame
- **Actionable**: Zusammenfassung muss für Neustart nutzbar sein
- **Vollständiger Kontext**: Alles was nötig ist um ohne diese Konversation weiterzumachen
- **Deutsch**: Alle Texte auf Deutsch
- **Code-Schnipsel**: Zeige relevanten Code, nicht nur beschreiben

## Integration mit Workflow

Nach dem Recovery:
1. Erwähne das Recovery-Dokument im nächsten `/dtb:workflow-checkpoint`
2. Nutze die Learnings fuer `/dtb:workflow-checkpoint`
3. Wenn nötig: Update `docs/lessons-learned.md` mit Pattern

## Wichtig

Eine Recovery-Analyse bedeutet **kein Scheitern** - es ist ein **professionelles Tool** um:
- Zeit zu sparen (nicht weiter im Kreis drehen)
- Learnings zu bewahren (nicht alles verwerfen)
- Strukturiert neu zu starten (mit besserem Kontext)

---

Analysiere jetzt die aktuelle Session und erstelle die Recovery-Dokumentation.
