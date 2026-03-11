# DTB Code Review

Führe ein professionelles Code Review mit Fokus auf kritische Issues durch.

## Wann verwenden?

- **Vor Commit**: Review von Änderungen vor dem Commit
- **Nach Feature**: Komplettes Feature wurde implementiert
- **Code Audit**: Bestehenden Code auf Probleme prüfen
- **Vor Deployment**: Final Check vor Production

## Aufgabe

Analysiere Code professionell mit Fokus auf **Business Impact** - priorisiert nach Schweregrad.

## Review-Prioritäten (in Reihenfolge)

1. 🔴 **Kritisch** - Logic Errors & Bugs → System-Ausfälle
2. 🔴 **Kritisch** - Security Vulnerabilities → Datenschutz-Probleme
3. 🟡 **Major** - Performance Problems → User Experience Impact
4. 🟡 **Major** - Maintainability Issues → Technische Schulden
5. 🔵 **Minor** - Code Style → Projekt-Standards

## Schritt 1: Kontext erfassen

Verwende das AskUserQuestion Tool um zu fragen:

1. **Was soll reviewt werden?**
   - Datei-Pfad(e)
   - Oder: Code direkt pasten

2. **Haupt-Anliegen?**
   - Security
   - Performance
   - Maintainability
   - Alles

3. **Spezifischer Fokus?**
   - Bestimmte Funktionen/Klassen
   - Neue Änderungen
   - Kompletter Code

## Schritt 2: Code lesen

Verwende das Read Tool um die spezifizierten Dateien zu lesen.

## Schritt 3: Review durchführen

Analysiere Code auf:
- **Business Logic Korrektheit**
- **Error Handling & Edge Cases**
- **Input Validation & Sanitization**
- **Impact auf bestehende Funktionalität**
- **Test Coverage & Qualität**

## Review-Report Format

Erstelle einen strukturierten Report:

```markdown
# Code Review Report: {TITEL}
**Datum:** {DD.MM.YYYY} | **Reviewer:** Claude
**Scope:** {Was wurde reviewt}

---

## 📊 Zusammenfassung

### Files Reviewed
{Liste der geprüften Dateien}

### Gesamt-Qualität
**Rating**: [🟢 Gut / 🟡 Akzeptabel / 🟠 Needs Work / 🔴 Kritische Issues]

### Issues-Übersicht
| Schweregrad | Anzahl | Status |
|-------------|--------|--------|
| 🔴 Kritisch | {N} | Muss gefixt werden |
| 🟡 Major | {N} | Sollte gefixt werden |
| 🔵 Minor | {N} | Optional |
| ✅ Positive | {N} | Good Practices |

---

## 🔴 Kritische Issues (MUSS gefixt werden)

### Issue #1: {Titel}

**Kategorie**: [Security / Bug / Data Loss]
**Datei**: `{pfad/zur/datei.py}`
**Zeile**: {X}

**Problem**:
{Was ist falsch? Konkret!}

**Impact**:
{Was könnte passieren? Business Impact!}

**Aktueller Code**:
```{language}
{problematischer Code mit Kontext}
```

**Vorgeschlagener Fix**:
```{language}
{korrigierter Code}
```

**Begründung**:
{Warum ist der Fix richtig?}

**Priorität**: 🔴 Sofort

---

### Issue #2: {Titel}
...

---

## 🟡 Major Issues (SOLLTE gefixt werden)

### Issue #1: {Titel}

**Kategorie**: [Performance / Maintainability / Code Quality]
**Datei**: `{pfad/zur/datei.py}`
**Zeile**: {X}

**Problem**:
{Beschreibung}

**Impact**:
{Auswirkung auf System/Team}

**Suggestion**:
{Verbesserungsvorschlag}

**Aufwand**: [Niedrig / Mittel / Hoch]

---

### Issue #2: {Titel}
...

---

## 🔵 Minor Issues (Kann gefixt werden)

### Issue #1: {Titel}

**Location**: `{datei}:{zeile}`
**Category**: [Style / Documentation / Naming]

**Suggestion**:
{Kleine Verbesserung}

**Beispiel**:
```{language}
# Aktuell
{current}

# Besser
{improved}
```

---

## 🔒 Security-Analyse

### Gefundene Vulnerabilities

| Severity | Issue | Location | OWASP Category |
|----------|-------|----------|----------------|
| 🔴 High | {Issue} | `{file}:{line}` | {Category} |
| 🟡 Medium | {Issue} | `{file}:{line}` | {Category} |

### Security Best Practices Check

- [x] ✅ **Input Validation**: Alle User-Inputs validiert
- [ ] ❌ **Output Encoding**: XSS-Gefahr in `{location}`
- [x] ✅ **Authentication**: Korrekt implementiert
- [ ] ⚠️ **Authorization**: Fehlt in `{endpoint}`
- [x] ✅ **Data Encryption**: Sensitive Daten verschlüsselt
- [ ] ❌ **SQL Injection**: Vulnerable Query in `{file}:{line}`
- [x] ✅ **CSRF Protection**: Implementiert
- [ ] ⚠️ **Rate Limiting**: Nicht implementiert

### Kritische Security-Probleme

#### Problem 1: SQL Injection
```python
# FALSCH ❌
query = f"SELECT * FROM users WHERE id = {user_id}"

# RICHTIG ✅
query = "SELECT * FROM users WHERE id = :id"
params = {"id": user_id}
```

---

## ⚡ Performance-Analyse

### Potenzielle Bottlenecks

| Issue | Location | Impact | Suggestion |
|-------|----------|--------|------------|
| {Issue} | `{file}:{line}` | {Impact} | {Fix} |

### Spezifische Probleme

#### Problem 1: N+1 Query
**Location**: `{file}:{line}`

```python
# Aktuell (N+1 Problem) ❌
for user in users:
    user.posts  # Separate Query für jeden User!

# Optimiert ✅
users = db.query(User).options(joinedload(User.posts)).all()
```

**Impact**: Bei 100 Users: 1 + 100 = 101 Queries statt 1
**Savings**: ~95% weniger DB-Calls

---

### Performance-Empfehlungen

1. **Caching hinzufügen**:
   - `{funktion}`: Result für {X} Minuten cachen
   - Erwartete Verbesserung: {Y}% schneller

2. **Index erstellen**:
   ```sql
   CREATE INDEX idx_{table}_{column} ON {table}({column});
   ```
   - Erwartete Verbesserung: Query {X}x schneller

---

## 🧹 Maintainability

### Code Smells

#### Smell #1: {Name}
**Location**: `{file}:{line}`
**Type**: [Long Method / Large Class / Duplicated Code / etc.]

**Problem**:
{Was macht den Code schwer wartbar?}

**Refactoring-Suggestion**:
```{language}
{Verbesserter Code}
```

**Benefit**: {Warum ist das besser?}

---

### Refactoring-Opportunities

#### Opportunity #1: Extract Method
**Current** (40 Zeilen Funktion):
```python
def process_user_data(data):
    # Validation (10 lines)
    ...
    # Processing (15 lines)
    ...
    # Storage (15 lines)
    ...
```

**Refactored**:
```python
def process_user_data(data):
    validated = validate_user_data(data)
    processed = transform_user_data(validated)
    return save_user_data(processed)
```

**Benefit**: Testbarkeit ⬆️, Lesbarkeit ⬆️

---

## 🧪 Test Coverage

### Fehlende Tests

**Ungetestete Scenarios**:
1. **{Scenario 1}**: {Beschreibung}
   - Warum kritisch: {Impact}
   - Test-Vorschlag: {Wie testen}

2. **{Scenario 2}**: {Beschreibung}
   ...

### Vorgeschlagene Test Cases

```{language}
describe('{Component}', () => {
  it('sollte {erwartetes Verhalten} bei {Bedingung}', () => {
    // Arrange
    {setup code}

    // Act
    {action}

    // Assert
    expect(result).toBe({expected})
  })

  it('sollte Fehler werfen bei {invalid input}', () => {
    expect(() => {action}).toThrow({ErrorType})
  })
})
```

### Edge Cases nicht getestet
- [ ] Empty input
- [ ] Null/undefined values
- [ ] Very large inputs
- [ ] Concurrent access
- [ ] Network failures

---

## ✨ Positive Beobachtungen

**Gut gemacht**:
- ✅ **{Practice 1}**: {Was gut ist und warum}
- ✅ **{Practice 2}**: {Was gut ist und warum}
- ✅ **Saubere Fehlerbehandlung**: Try-catch korrekt implementiert
- ✅ **Type Hints**: Alle Funktionen haben Type Annotations

---

## 📋 Action Items

### 🔴 Sofort (Vor Merge/Deploy)
- [ ] **Fix Issue #1**: {Kurzbeschreibung}
- [ ] **Fix Issue #2**: {Kurzbeschreibung}
- [ ] **Security**: {Critical Security Fix}

### 🟡 Kurzfristig (Diese Woche)
- [ ] **Performance**: {Optimization}
- [ ] **Refactoring**: {Code Smell beheben}
- [ ] **Tests**: {Fehlende Tests hinzufügen}

### 🔵 Langfristig (Tech Debt)
- [ ] **Refactoring**: {Größeres Refactoring}
- [ ] **Documentation**: {Docs verbessern}
- [ ] **Architecture**: {Strukturelle Verbesserung}

---

## 📝 Review-Notizen

### Positives
{Was wurde gut gemacht?}

### Bedenken
{Wo gibt es Zweifel?}

### Fragen an Developer
1. {Frage zu Design-Entscheidung}
2. {Frage zu Implementation}

---

## ✅ Sign-Off

### Aktueller Status
- [ ] ❌ **Nicht merge-bereit** - Kritische Issues müssen gefixt werden
- [ ] ⚠️ **Bedingt approved** - Major Issues sollten vor Merge gefixt werden
- [ ] ✅ **Approved** - Kann gemerged werden, Minor Issues optional

### Nächste Schritte
1. {Konkreter nächster Schritt}
2. {Konkreter nächster Schritt}

### Follow-up Review nötig?
- [ ] Ja, nach Fixes
- [ ] Nein, nur Minor Issues

---

**Reviewer**: Claude
**Datum**: {DD.MM.YYYY HH:MM}
```

## Speicherung

Speichere den Review-Report mit dem Write Tool:
- Pfad: `docs/reviews/YYYY-MM-DD-{component}-review.md`
- Falls `docs/reviews/` nicht existiert, erstelle es

## Richtlinien

- **Significant Issues only**: Nur wichtige Probleme, die Action benötigen
- **Spezifisch & Actionable**: Konkrete Verbesserungsvorschläge mit Code
- **Code-Beispiele**: Zeige immer Vorher/Nachher Code
- **Positives erwähnen**: Nicht nur Kritik, auch Lob
- **Business Impact**: Priorisiere nach tatsächlichem Impact
- **Deutsch**: Alle Texte auf Deutsch

## Security-Fokus (OWASP Top 10)

Prüfe besonders auf:
1. **Injection** (SQL, Command, XSS)
2. **Broken Authentication**
3. **Sensitive Data Exposure**
4. **XML External Entities (XXE)**
5. **Broken Access Control**
6. **Security Misconfiguration**
7. **Cross-Site Scripting (XSS)**
8. **Insecure Deserialization**
9. **Using Components with Known Vulnerabilities**
10. **Insufficient Logging & Monitoring**

## Integration mit Workflow

Nach dem Review:
1. **Session-Log**: Erwähne Review in `/dtb:workflow-checkpoint`
2. **Action Items**: Füge kritische Fixes zu Session "Nächste Schritte" hinzu
3. **Backlog**: Review-Ergebnisse pruefen mit `/dtb:backlog`

## Wichtig

Ein gutes Code Review:
- ✅ Findet echte Probleme, nicht nur Stil-Fragen
- ✅ Hilft Team zu lernen (erkläre das "Warum")
- ✅ Ist konstruktiv, nicht destruktiv
- ✅ Spart Zeit durch frühe Problem-Erkennung

---

Führe jetzt das Code Review durch für den angegebenen Code.
