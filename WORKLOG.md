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

### Agent-Teams: Zwei Rollen reichen
**Kontext:** Beim Design von `/dtb:epic-review` habe ich mir das BMAD-Framework angeschaut — dort gibt es 5 Rollen (Bob, Alice, Charlie, Dana, Elena). Das ist fuer ein Solo-Projekt nicht realistisch: kein QA-Team, keine Junior-Devs, kein Scrum-Master noetig.

**Rollenaufteilung die funktioniert:**

| Rolle | Warum | Was sie tut |
|-------|-------|-------------|
| Architekt | Prueft ob der Feature-Plan technisch solide ist | Abhaengigkeiten, Risiken, fehlende Schritte |
| Pragmatiker | Haelt den Scope realistisch | "Zu gross", "Phase 2 reicht erstmal", MVP-Schnitt |
| Du (Damian) | Entscheidungshoheit + Domain-Wissen | Wirst gefragt, gibst Kontext, entscheidest |

**Kerngedanke:** Damian ist nicht ein weiterer Agent — er ist der Product Owner. Die Agenten diskutieren, stellen gezielt Fragen ("Damian, brauchst du Feature X wirklich in Phase 1?"), und er entscheidet. Ein Koordinator/Scrum-Master ist bei 2 Agenten + PO unnoetig — das waere Over-Engineering.

**Prinzip:** Weniger Rollen = klarere Verantwortung. Lieber mit 2 fokussierten Perspektiven starten und bei Bedarf erweitern, als sofort ein komplexes Agenten-Orchester aufzubauen. Die dritte Rolle (Koordination) ergibt sich natuerlich aus der PO-Rolle.

### Skills statt Commands — eine Variante reichen lassen
**Erkenntnis:** Wir hatten Commands und Skills parallel gepflegt — identischer Inhalt, doppelte Arbeit. Skills koennen alles was Commands koennen, plus Trigger-basierte Erkennung durch YAML-Frontmatter. Die Commands boten keinen Mehrwert.

**Warum:** Doppelpflege fuehrt unweigerlich zu Drift. Wenn zwei Dateien denselben Inhalt haben, wird eine irgendwann veraltet sein. Lieber eine Single Source of Truth waehlen und konsequent dabei bleiben. Skills sind die maechtigere Variante — Commands wurden entfernt.

### Ideen sofort einfangen, spaeter ausarbeiten
**Erkenntnis:** Waehrend der Arbeit kommen staendig Gedanken und Ideen. Ohne einen schnellen Weg sie festzuhalten, gehen sie verloren oder unterbrechen den Flow. Die Loesung: `/dtb:idea` fuer sofortiges Erfassen (Freitext, keine Rueckfragen), `/dtb:idea-review` fuer spaeteres Sichten, und `/dtb:feature-plan` greift offene Ideen automatisch auf.

**Warum:** Der Schluessel ist die Trennung von Erfassen und Ausarbeiten. Beim Erfassen zaehlt Geschwindigkeit — kein Formular, keine Kategorisierung, kein Workflow. Die Struktur kommt spaeter, wenn man bewusst Zeit dafuer nimmt. So bleibt der aktuelle Arbeitsfluss ungestoert.
