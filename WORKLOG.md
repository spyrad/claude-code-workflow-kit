# Worklog — Erfahrungen, Gedanken & Prinzipien

Persoenliches Log zu Arbeitsweise, Erkenntnissen und Ideen rund um Claude Code und dieses Toolkit.

---

## Arbeits-Prinzipien

### Entstehung: Workflow aus der Praxis, nicht aus der Theorie
**Erkenntnis:** Die Skills in diesem Toolkit sind nicht von einem Framework uebernommen oder theoretisch entworfen worden. Sie sind waehrend der taeglichen Projektarbeit mit einem AI-Assistenten entstanden — Stueck fuer Stueck, aus echten Momenten heraus:

- "Diesen Schritt mache ich jedes Mal von Hand" → Skill draus bauen
- "Braucht es hier wirklich mein Feedback oder kann das automatisch laufen?" → Autonomie-Level definieren
- "Es waere praktisch, das kurz irgendwo zu dokumentieren" → Session-Log / Checkpoint
- "In welchem Schritt wird diese Notiz spaeter wieder gebraucht?" → Inbox → Feature-Plan Pipeline

**Warum das wichtig ist:** Dieser Bottom-up-Ansatz fuehrt zu Skills, die tatsaechlich genutzt werden — weil sie ein reales Problem loesen, das beim Arbeiten aufgefallen ist. Kein theoretisches Workflow-Design im Voraus, sondern beobachten, was sich wiederholt, und dann erst automatisieren.

### Wiederholte Prompts → Automatisieren
**Erkenntnis:** Sobald ein Prompt mehr als einmal benutzt wird, lohnt es sich zu pruefen, ob daraus ein Skill entstehen sollte.

**Warum:** Wiederholung ist ein Signal fuer ein wiederkehrendes Muster. Skills machen diese Muster wiederverwendbar, konsistent und teilbar — statt jedes Mal den Prompt neu zu formulieren.

### Dokumentation aktuell halten
**Erkenntnis:** CLAUDE.md, MEMORY.md und Status-Dateien muessen den tatsaechlichen Projektzustand widerspiegeln. Veraltete Eintraege (z.B. "noch nicht begonnen" obwohl ein Feature laengst fertig ist) fuehren dazu, dass Claude auf falschem Kontext arbeitet und falsche Entscheidungen trifft.

**Warum:** Diese Dateien sind Claudes primaere Informationsquelle beim Gespraechsstart. Stimmt der Inhalt nicht mit der Realitaet ueberein, entstehen Folgefehler — falsche Priorisierungen, redundante Arbeit, oder Vorschlaege die am aktuellen Stand vorbeigehen. Regelmaessiges Abgleichen (z.B. beim Workflow-Checkpoint) ist essentiell.

### Kontext-Qualitaet vor Quantitaet
**Erkenntnis:** Der Agent ist nur so gut wie der Kontext, den wir ihm geben. Gleichzeitig geht es nicht um Quantitaet, sondern um Qualitaet und Aktualitaet. Deswegen ist es wichtig, die Informations- und Kontextdateien aktuell zu halten und in einer fuer AI optimalen Groesse zu pflegen.

**Warum:** Zu viel Kontext verwässert die relevanten Informationen — zu wenig oder veralteter Kontext fuehrt zu falschen Annahmen. Die Kunst liegt darin, dem Agenten genau das zu geben, was er braucht: aktuell, kompakt und praezise.

### Klein anfangen statt Framework-Overkill
**Erkenntnis:** Da draussen gibt es jede Menge Frameworks, die zwar alles abdecken und sexy aussehen, aber letztendlich selten wirklich produktiv eingesetzt werden. Zu komplex, Lernkurve zu steil, unuebersichtlich.

Deswegen habe ich angefangen, mit einzelnen Schritten zu arbeiten, die mich tatsaechlich bei der Arbeit unterstuetzen — und so meinen Workflow Stueck fuer Stueck aufzubauen. Das kann jeder fuer sich bauen oder einzelne Schritte uebernehmen.

**Warum es sich lohnt:** Das ist ein schneller Weg zur Automatisierung aller Routinen, die tatsaechlich automatisch oder zumindest halbautomatisch ablaufen koennen. Kein theoretisches Framework-Studium noetig — einfach anfangen, was funktioniert behalten, was nicht passt anpassen.

### Agent-Teams: Drei fokussierte Perspektiven
**Kontext:** Beim Design von `/dtb:plan-review` habe ich mir das BMAD-Framework angeschaut — dort gibt es 5 Rollen (Bob, Alice, Charlie, Dana, Elena). Das ist fuer ein Solo-Projekt nicht realistisch: kein QA-Team, keine Junior-Devs, kein Scrum-Master noetig. Aber drei fokussierte Perspektiven decken die relevanten Aspekte eines Implementierungsplan-Reviews ab.

**Rollenaufteilung die funktioniert:**

| Rolle | Warum | Was sie tut |
|-------|-------|-------------|
| Architekt | Prueft ob der Plan systemisch solide ist | Abhaengigkeiten, Risiken, Systemgrenzen, Edge Cases |
| Pragmatiker | Haelt den Scope realistisch | "Zu gross", "Phase 2 reicht erstmal", MVP-Schnitt |
| Senior Dev | Prueft die technische Umsetzbarkeit | Realistische Zeitschaetzungen, Teststrategie, fehlende Migrationen/Schritte auf Code-Ebene |
| Du (Damian) | Entscheidungshoheit + Domain-Wissen | Wirst gefragt, gibst Kontext, entscheidest |

**Kerngedanke:** Damian ist nicht ein weiterer Agent — er ist der Product Owner. Die Agenten diskutieren, stellen gezielt Fragen ("Damian, brauchst du Feature X wirklich in Phase 1?"), und er entscheidet. Ein Koordinator/Scrum-Master ist bei 3 Agenten + PO unnoetig — das waere Over-Engineering.

**Warum drei und nicht zwei:** Der Senior Dev ist kein Koordinator, sondern bringt eine eigenstaendige Perspektive: die Code-Level-Machbarkeit. Architekt denkt in Systemen, Pragmatiker denkt in Scope — aber keiner prueft ob die Schritte im Plan tatsaechlich so umsetzbar sind, ob Zeitschaetzungen realistisch sind, oder ob eine Teststrategie fehlt. Diese Luecke schliesst der Senior Dev.

**Prinzip:** Jede Rolle muss eine eigene, nicht-redundante Perspektive haben. Keine Rolle "zur Sicherheit" — nur Rollen die eine echte Luecke schliessen.

### Skills statt Commands — eine Variante reichen lassen
**Erkenntnis:** Wir hatten Commands und Skills parallel gepflegt — identischer Inhalt, doppelte Arbeit. Skills koennen alles was Commands koennen, plus Trigger-basierte Erkennung durch YAML-Frontmatter. Die Commands boten keinen Mehrwert.

**Warum:** Doppelpflege fuehrt unweigerlich zu Drift. Wenn zwei Dateien denselben Inhalt haben, wird eine irgendwann veraltet sein. Lieber eine Single Source of Truth waehlen und konsequent dabei bleiben. Skills sind die maechtigere Variante — Commands wurden entfernt.

### Ideen sofort einfangen, spaeter ausarbeiten
**Erkenntnis:** Waehrend der Arbeit kommen staendig Gedanken und Ideen. Ohne einen schnellen Weg sie festzuhalten, gehen sie verloren oder unterbrechen den Flow. Die Loesung: `/dtb:idea` fuer sofortiges Erfassen (Freitext, keine Rueckfragen), `/dtb:idea-review` fuer spaeteres Sichten, und `/dtb:feature-plan` greift offene Ideen automatisch auf.

**Warum:** Der Schluessel ist die Trennung von Erfassen und Ausarbeiten. Beim Erfassen zaehlt Geschwindigkeit — kein Formular, keine Kategorisierung, kein Workflow. Die Struktur kommt spaeter, wenn man bewusst Zeit dafuer nimmt. So bleibt der aktuelle Arbeitsfluss ungestoert.

### Kleine Funktionen bauen statt jedes Mal von vorne beschreiben
**Erkenntnis:** Es lohnt sich, in kleinen wiederverwendbaren Funktionen zu denken — anstatt jedes Mal ausfuehrlich und manuell von Neuem zu beschreiben, was passieren soll, lieber ein kleines System bauen, das eine Funktionalitaet abbildet. Skills sind genau das: kompakte, wiederverwendbare Bausteine fuer wiederkehrende Aufgaben.

**Der springende Punkt:** Mit Claude als Arbeitsbuddy geht das einfach und schnell. Man beschreibt einmal, was man braucht, und hat in Minuten einen funktionierenden Skill. Kein aufwaendiges Framework-Design, kein Boilerplate — einfach bauen, testen, nutzen.

**Fuer andere:** Wer sich das claude-code-workflow-kit runterlaedt, wird feststellen: Claude versteht die Struktur sofort — und genauso dein Projekt. Claude beurteilt, was zu deiner Arbeitsweise passt und was nicht, nimmt dich an die Hand und zeigt, wo die Skills gleich einen Mehrwert liefern und wo man sie an deine Arbeitsweise anpassen sollte. Der Einstieg ist nicht "lies die Doku", sondern "starte Claude und lass dir zeigen, was fuer dich funktioniert".

### Implizites Wissen explizit und maschinenlesbar machen
**Erkenntnis:** Die Pipeline zwischen den Skills war immer schon da — verteilt ueber Freitext in "Naechste Schritte" und "Verwandte Commands". Aber kein Skill wusste maschinell, wo er in der Kette steht, was er konsumiert oder produziert. Durch das Pipeline-Frontmatter (`after`, `next`, `consumes`, `produces`) wird aus implizitem Wissen strukturierte Daten, die Tools wie `project-health` automatisch validieren koennen.

**Prinzip:** Wenn etwas eine Struktur hat, sollte es auch als Struktur abgebildet sein — nicht als Prosa. Prosa ist fuer Menschen gut lesbar, aber ein Tool kann damit nichts anfangen. Strukturierte Metadaten ermoeglichen automatische Konsistenzpruefungen, Visualisierungen und Fehlererkennung — Dinge, die bei Prosa manuell passieren muessten.

**Konkretes Beispiel:** Vorher stand in einem Skill "Naechster Schritt: /dtb:impl-plan". Jetzt steht im Frontmatter `next: dtb:impl-plan` — und `project-health` kann pruefen, ob dieser Skill tatsaechlich existiert, ob die Rueckrichtung stimmt, und ob es zirkulaere Referenzen gibt. Gleicher Inhalt, aber maschinenlesbar.

### Sub-CLAUDE.md als kontextuelle Doku-Schichten
**Erkenntnis:** Die Root-CLAUDE.md wird bei jeder Conversation geladen und sollte deshalb schlank bleiben (<150 Zeilen). Aber bereichsspezifische Konventionen muessen trotzdem irgendwo dokumentiert sein — z.B. wie man einen neuen Skill schreibt oder wie Agent-Dateien strukturiert sein muessen.

**Loesung:** Sub-CLAUDE.md Dateien in Unterverzeichnissen (`skills/CLAUDE.md`, `agents/CLAUDE.md`). Diese werden nur geladen, wenn Claude in dem jeweiligen Verzeichnis arbeitet. So bekommt der Agent die richtigen Regeln genau dann, wenn er sie braucht — ohne die Root-Datei aufzublaehen.

**Warum das funktioniert:** Claude Code laedt CLAUDE.md Dateien kontextabhaengig — die Root-Datei immer, Sub-Dateien nur wenn im entsprechenden Verzeichnis gearbeitet wird. Das ist ein natuerlicher Mechanismus fuer geschichtete Dokumentation: allgemeine Regeln oben, spezifische Details dort wo sie gebraucht werden.
