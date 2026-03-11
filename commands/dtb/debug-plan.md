# DTB Debug Action Plan

Erstelle einen strukturierten Untersuchungs- und Lösungsplan für Bugs und technische Probleme.

## Wann verwenden?

- Bug wurde gemeldet oder entdeckt
- Feature funktioniert nicht wie erwartet
- Performance-Problem identifiziert
- Fehler tritt auf, aber Ursache unklar

## Aufgabe

Erstelle einen systematischen Debug-Plan mit Untersuchungsschritten, Code-Analyse und Root-Cause-Hypothesen.

## Schritt 1: Problem erfassen

Verwende das AskUserQuestion Tool um zu fragen:

1. **Problem-Beschreibung**: Was funktioniert nicht? (Konkrete Symptome)
2. **Reproduzierbarkeit**:
   - Immer
   - Manchmal (Muster?)
   - Nur unter bestimmten Bedingungen
3. **Erwartetes vs. Tatsächliches Verhalten**
4. **Kontext**:
   - Wann tritt es auf?
   - Welche Component/Modul betroffen?
   - Letzte Änderungen in dem Bereich?

## Schritt 2: Relevanten Code analysieren

Lese mit dem Read Tool:
- Betroffene Dateien (basierend auf Problem-Beschreibung)
- Verwandte Module/Funktionen
- Konfigurationsdateien (falls relevant)
- Logs (falls vorhanden)

## Schritt 3: Git-History prüfen

Falls hilfreich:
```bash
# Letzte Änderungen an betroffener Datei
git log --oneline -- pfad/zur/datei.py

# Wann wurde diese Funktion zuletzt geändert?
git log -p --all -S "function_name"

# Diff anzeigen
git show <commit-hash>
```

## Schritt 4: Debug-Plan erstellen

Erstelle einen strukturierten Plan in diesem Format:

```markdown
# Debug Action Plan: {PROBLEM-TITEL}
**Datum:** {DD.MM.YYYY} | **Zeit:** {HH:MM}
**Status:** 🔴 Offen | **Priorität**: [Hoch/Mittel/Niedrig]

---

## 🐛 Problem-Beschreibung

### Symptome
{Was genau ist das beobachtbare Problem? Konkret!}

### Erwartetes Verhalten
{Was sollte passieren?}

### Tatsächliches Verhalten
{Was passiert stattdessen?}

### Reproduktions-Schritte
1. {Schritt 1}
2. {Schritt 2}
3. {Schritt 3}
4. **Ergebnis**: {Fehlerbeschreibung}

### Reproduzierbarkeit
- [ ] Immer reproduzierbar
- [ ] Sporadisch ({Muster wenn bekannt})
- [ ] Nur unter Bedingungen: {Bedingungen}

---

## 📋 Umgebungs-Information

### System
- **OS**: {Betriebssystem}
- **Runtime**: {Python 3.x / Node 20.x / etc.}
- **Environment**: {Development / Test / Production}

### Relevante Versionen
- **{Package}**: {Version}
- **{Framework}**: {Version}

### Konfiguration
```yaml
{Relevante Config-Werte}
```

---

## 🔍 Betroffene Code-Bereiche

### Primär verdächtig
- **Datei**: `{pfad/zur/datei.py}`
- **Funktion/Klasse**: `{function_name}` (Zeile {X})
- **Warum verdächtig**: {Begründung}

### Sekundär verdächtig
- **Datei**: `{pfad/zur/datei2.py}`
- **Zusammenhang**: {Wie hängt es mit Primary zusammen?}

### Abhängigkeiten
```
{Komponente A} → {Komponente B} → {Komponente C}
                          ↓
                    (Problem hier?)
```

---

## 📊 Git-History Analyse

### Letzte Änderungen (verdächtig)
| Commit | Datum | Autor | Änderung |
|--------|-------|-------|----------|
| `{hash}` | {Datum} | {Name} | {Beschreibung} |

### Relevante Commits
```bash
# Commit {hash} - {Titel}
{Kurze Zusammenfassung der Änderung}

# Verdacht
{Könnte dieser Commit das Problem verursacht haben? Warum?}
```

---

## 💡 Root Cause Hypothesen

### Hypothese 1: {Titel} (⭐ Wahrscheinlichste)
- **Theorie**: {Was könnte die Ursache sein?}
- **Evidence**: {Welche Beobachtungen stützen diese Theorie?}
- **Code-Location**: `{datei}:{zeile}`
- **Test-Ansatz**: {Wie kann man diese Hypothese testen?}

### Hypothese 2: {Titel}
- **Theorie**: {Alternative Erklärung}
- **Evidence**: {Supporting facts}
- **Code-Location**: `{datei}:{zeile}`

### Hypothese 3: {Titel}
...

---

## 🔬 Untersuchungs-Plan

### Phase 1: Informationen sammeln
- [ ] **Log-Analyse**: {Welche Logs checken?}
  - Location: `{pfad/zu/logs}`
  - Suche nach: `{Keywords}`

- [ ] **Debugging aktivieren**: {Debug-Mode einschalten}
  ```bash
  {Command für Debug-Mode}
  ```

- [ ] **Breakpoints setzen**: {Wo genau debuggen?}
  - `{datei}:{zeile}` - {Warum hier?}
  - `{datei}:{zeile}` - {Warum hier?}

### Phase 2: Hypothesen testen

#### Test für Hypothese 1
```python
# Testcode oder manuelle Schritte
{Code zum Testen der Hypothese}
```

**Erwartetes Ergebnis wenn Hypothese richtig**:
{Was würde man sehen?}

#### Test für Hypothese 2
...

### Phase 3: Isolierung
- [ ] **Minimal reproduzierbares Beispiel erstellen**
  ```{language}
  {Minimaler Code der das Problem zeigt}
  ```

- [ ] **Variable Faktoren eliminieren**:
  - {Faktor 1}: Testen mit/ohne
  - {Faktor 2}: Verschiedene Werte probieren

---

## 🛠️ Mögliche Lösungsansätze

### Ansatz 1: {Titel} (Wenn Hypothese 1 richtig)
**Änderungen**:
```{language}
# Aktueller Code
{problematischer Code}

# Vorgeschlagene Änderung
{korrigierter Code}
```

**Begründung**: {Warum löst das das Problem?}

**Risiken**: {Könnte das andere Dinge kaputt machen?}

**Test**: {Wie validieren dass es funktioniert?}

---

### Ansatz 2: {Titel} (Wenn Hypothese 2 richtig)
...

---

## 📝 Debug-Notizen

### Versuch 1: {Beschreibung}
- **Durchgeführt**: {Datum/Zeit}
- **Aktion**: {Was wurde getestet?}
- **Ergebnis**: {Was kam raus?}
- **Learnings**: {Was haben wir gelernt?}

### Versuch 2: {Beschreibung}
...

---

## ✅ Validierungs-Checklist

Nach dem Fix:
- [ ] Problem ist reproduzierbar behoben
- [ ] Unit Tests passen (oder neue erstellt)
- [ ] Keine Regressions in anderen Features
- [ ] Code Review durchgeführt
- [ ] Dokumentation aktualisiert (falls nötig)
- [ ] Root Cause dokumentiert

---

## 🎯 Nächste Schritte

### Sofort
1. {Konkreter nächster Schritt}
2. {Konkreter nächster Schritt}

### Falls Stuck
- {Alternative Untersuchungs-Methode}
- {Person/Ressource die helfen könnte}

### Eskalation
Falls nicht lösbar in {X} Stunden:
- [ ] {Eskalations-Plan}

---

## 📚 Referenzen

### Relevante Dokumentation
- `{docs/file.md}`: {Was steht dort?}

### Ähnliche Probleme (wenn bekannt)
- Issue #{N}: {Kurzbeschreibung}
- Commit {hash}: {Ähnlicher Fix}

### Externe Ressourcen
- {Link zu Stack Overflow / Dokumentation}

---

## 📊 Tracking

**Zeitaufwand (Schätzung)**:
- Investigation: ~{X} Stunden
- Fix Implementation: ~{X} Stunden
- Testing: ~{X} Stunden
- **Total**: ~{X} Stunden

**Status Updates**:
- {Zeit}: {Status-Update}

---

## 🔄 Post-Mortem (nach Lösung)

### Was war die Root Cause?
{Tatsächliche Ursache nach Lösung}

### Wie wurde es gelöst?
```{language}
{Actual fix code}
```

### Lessons Learned
- {Learning 1}: {Für Zukunft merken}
- {Learning 2}

### Prävention
Wie kann man das in Zukunft verhindern?
- {Maßnahme 1}
- {Maßnahme 2}
```

## Speicherung

Speichere den Debug-Plan mit dem Write Tool:
- Pfad: `docs/debug/YYYY-MM-DD-{kurztitel}.md`
- Falls `docs/debug/` nicht existiert, erstelle es

## Richtlinien

- **Systematisch**: Strukturierter Ansatz, nicht wild rumprobieren
- **Dokumentiere alles**: Jeder Versuch wird notiert
- **Hypothesen-getrieben**: Teste spezifische Theorien
- **Code-konkret**: Zeige tatsächlichen Code, nicht nur Beschreibungen
- **Deutsch**: Alle Texte auf Deutsch
- **Iterativ**: Plan kann während Debug erweitert werden

## Integration mit Workflow

Während des Debuggings:
1. **Update den Plan**: Füge Debug-Notizen zu jedem Versuch hinzu
2. **Session-Log**: Erwähne den Debug-Plan in `/dtb:workflow-checkpoint`
3. **Nach Lösung**: Post-Mortem ausfüllen für Lessons Learned

## Wichtig

Ein guter Debug-Plan:
- ✅ Spart Zeit durch systematisches Vorgehen
- ✅ Verhindert "Trial & Error" ohne Struktur
- ✅ Dokumentiert den Lösungsweg (für ähnliche Probleme)
- ✅ Macht Fortschritt messbar

---

Erstelle jetzt den Debug Action Plan für das beschriebene Problem.
