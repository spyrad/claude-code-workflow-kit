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

### Fuer die AI denken, nicht fuer Menschen dokumentieren
**Erkenntnis:** Beim Erstellen von Skills, Rules und Kontext-Dateien ist die entscheidende Frage nicht "Wie wuerde ein Mensch das lesen?", sondern "Was braucht die AI, um optimal zu arbeiten?". Das bedeutet: keine ausfuehrlichen Manuals oder Erklaerungstexte, sondern schmale, gezielte Informationen — kompakt, strukturiert, direkt umsetzbar.

**Warum:** Die AI liest keine Doku zum Verstaendnis — sie braucht klare Anweisungen, Regeln und Kontext um Entscheidungen zu treffen. Lange Erklaerungen verwaessern den Fokus, kurze Regeln mit Begruendung sind sofort anwendbar. Ein "Do: X, weil Y" ist fuer die AI wertvoller als drei Absaetze Hintergrund.

**Konkret:** Rules-Dateien in `project-rules/` sollten keine Coding-Handbuecher sein, sondern knappe Checklisten: Was gilt, warum, und ein Beispiel-Pfad. Dasselbe Prinzip gilt fuer CLAUDE.md, Memory-Dateien und Skill-Templates — immer fragen: "Ist das fuer die AI nuetzlich oder nur fuer menschliche Leser huebsch?"

### Lern-Feedback-Loop: Erkenntnisse maschinell zurückführen
**Erkenntnis:** Es gab lange ein `pitfalls.md`-Template im Memory-Framework — aber kein Skill hat es je gelesen. Erkenntnisse landeten nur im Session-Log und wurden nie wieder aktiv herangezogen: totes Wissen. Der Skill `dtb:lesson` schließt den Kreis: Lektionen werden append-only in `lessons.md` erfasst (manuell oder als Agent-Vorschlag, immer mit Bestätigung) und von den Plan-/Review-Skills als Prior gelesen und angewandt.

**Warum:** Wissen festzuhalten reicht nicht — es muss an der Stelle wieder auftauchen, wo es gebraucht wird. Erfassen ohne Rückführung ist ein Archiv, das niemand liest. Der Hebel liegt im *maschinell gelesenen Prior*: nicht der Mensch muss sich erinnern, der nächste Skill-Lauf bringt die relevante Regel selbst mit. Das ist die aktive Variante von "implizites Wissen explizit machen".

**Abgrenzung, die den Loop trägt:** Session-Log = "was ist diese Session passiert" (vergänglich); Lektion = "Regel, die künftig gilt" (dauerhaft). Trigger-Frage beim Vorschlagen: "Würde ich denselben Fehler nochmal machen, wenn das nur im Session-Log stünde?"

### Status ableiten statt speichern
**Erkenntnis:** Statusfelder, die man von Hand pflegt, driften unweigerlich ("noch nicht begonnen", obwohl längst fertig). Die Lösung (Feature Derived State): Status wird nicht gespeichert, sondern aus Artefakten *abgeleitet* — Existenz von DISCOVERY/FEATURE/PLAN plus die `## Progress`-Checkboxen sind die einzige Wahrheit. Statusfelder in BACKLOG/WORKFLOW_STATUS sind nur abgeleitete Anzeigen.

**Warum:** Zwei Quellen für dieselbe Information erzeugen garantiert irgendwann Widerspruch. Eine einzige Quelle der Wahrheit plus mechanische Ableitung eliminiert die Drift an der Wurzel. Wichtig ist die Konfliktregel: bei Widerspruch gewinnt das Artefakt, und der Widerspruch wird *gemeldet* statt still übergangen — so bleibt der Mechanismus vertrauenswürdig.

### Distribution braucht einen dritten Fixpunkt
**Erkenntnis:** Der Schmerz war real und wiederholt: `workflow-resume` lief einmal unbemerkt mit einer veralteten installierten Skill-Kopie. Ein einfacher Zwei-Wege-Vergleich (Repo ↔ Kopie) kann nur sagen *dass* etwas abweicht, nicht *in welche Richtung*. `kit-sync` führt mit dem Lock einen dritten Fixpunkt ein: Repo ↔ Lock ↔ Kopie macht die Drift-Richtung diagnostizierbar — "Repo weitergezogen" vs. "lokal geändert" vs. "beide" sind unterscheidbare Zustände mit je eigener Aktion.

**Warum:** Ein Abgleich, der die Richtung nicht kennt, muss raten oder fragen — und rät im Zweifel falsch. Der dritte Fixpunkt (was war beim letzten Sync installiert?) verwandelt ein mehrdeutiges "unterschiedlich" in eine eindeutige Diagnose. Das ist der Unterschied zwischen "irgendwas stimmt nicht" und "spiel Update X ein, Kopie Y ist bewusst abweichend".

### Spike statt Annahme
**Erkenntnis:** Bei `kit-sync` war die Hash-Methode zunächst eine Annahme ("`git hash-object` reicht"). Ein kurzer Spike zeigte: `git hash-object` ist config-abhängig (`autocrlf`) — dieselbe Datei liefert je nach Maschine unterschiedliche Hashes. Erst die verbindliche Methode (`tr -d '\r' | git -c core.autocrlf=false hash-object --stdin`) macht LF/CRLF-Kopien korrekt gleich.

**Warum:** Eine falsche Annahme im Fundament (Hashing) hätte den gesamten Drift-Vergleich unzuverlässig gemacht — auf jeder anderen Maschine falsch. Fünf Minuten Spike sind billiger als ein Mechanismus, der subtil und plattformabhängig lügt. Der Review (Senior Dev) hatte genau hier nachgehakt — Annahmen an der Systemgrenze gehören verifiziert, nicht geglaubt.

### Unabhängige, kontextlose Abnahme findet echte Fehler
**Erkenntnis:** Die Abnahme von DERIVED_STATE, KIT_SYNC und LESSON_LOOP lief jeweils über einen unabhängigen Agenten *ohne* Session-Kenntnis, der nur den geschriebenen Stand gegen Szenarien prüft. Bei LESSON_LOOP fand dieser Agent einen echten Bug, den der Autor übersah: ein `|` im Feldinhalt (Shell-Pipe im Beispiel) zerschießt die Markdown-Tabelle und damit alle nachgelagerten Filter.

**Warum:** Wer etwas gebaut hat, liest das Gemeinte, nicht das Geschriebene — blinde Flecken sind systematisch, nicht zufällig. Ein Agent ohne Kontext befolgt die Anweisung wörtlich und stolpert genau dort, wo eine echte Nutzung stolpern würde. Die fehlende Vorkenntnis ist hier das Feature, nicht ein Mangel.

### Parallele Arbeitsstränge sauber trennen
**Erkenntnis:** Während LESSON_LOOP lief, wurde parallel ein zweites Feature (Betriebs-Wächter) an teils denselben Dateien gebaut (`plan-review`). Statt beides zu vermischen: die fremden Änderungen erkennen und *surfacen*, nicht blind mitcommitten — und pro Strang einen eigenen, thematisch sauberen Commit machen (die geteilte Datei `plan-review` bewusst dem passenden Strang zugeordnet).

**Warum:** Ein Commit, der zwei unfertige Themen vermischt, ist weder reviewbar noch rückbaubar — und referenziert schlimmstenfalls Dateien, die er selbst nicht enthält. Die Disziplin "was gehört zu welchem Scope?" vor jedem `git add` hält die Historie lesbar. Und: uncommittete Fremdänderungen im Working Tree sind ein Signal, kein Rauschen — erst verstehen, dann committen.
