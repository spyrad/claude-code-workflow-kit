# Worklog — Erfahrungen, Gedanken & Prinzipien

Persönliches Log zu Arbeitsweise, Erkenntnissen und Ideen rund um Claude Code und dieses Toolkit.

---

## Arbeits-Prinzipien

### Entstehung: Workflow aus der Praxis, nicht aus der Theorie
**Erkenntnis:** Die Skills in diesem Toolkit sind nicht von einem Framework übernommen oder theoretisch entworfen worden. Sie sind während der täglichen Projektarbeit mit einem AI-Assistenten entstanden — Stück für Stück, aus echten Momenten heraus:

- "Diesen Schritt mache ich jedes Mal von Hand" → Skill draus bauen
- "Braucht es hier wirklich mein Feedback oder kann das automatisch laufen?" → Autonomie-Level definieren
- "Es wäre praktisch, das kurz irgendwo zu dokumentieren" → Session-Log / Checkpoint
- "In welchem Schritt wird diese Notiz später wieder gebraucht?" → Inbox → Feature-Plan Pipeline

**Warum das wichtig ist:** Dieser Bottom-up-Ansatz führt zu Skills, die tatsächlich genutzt werden — weil sie ein reales Problem lösen, das beim Arbeiten aufgefallen ist. Kein theoretisches Workflow-Design im Voraus, sondern beobachten, was sich wiederholt, und dann erst automatisieren.

### Wiederholte Prompts → Automatisieren
**Erkenntnis:** Sobald ein Prompt mehr als einmal benutzt wird, lohnt es sich zu prüfen, ob daraus ein Skill entstehen sollte.

**Warum:** Wiederholung ist ein Signal für ein wiederkehrendes Muster. Skills machen diese Muster wiederverwendbar, konsistent und teilbar — statt jedes Mal den Prompt neu zu formulieren.

### Dokumentation aktuell halten
**Erkenntnis:** CLAUDE.md, MEMORY.md und Status-Dateien müssen den tatsächlichen Projektzustand widerspiegeln. Veraltete Einträge (z.B. "noch nicht begonnen" obwohl ein Feature längst fertig ist) führen dazu, dass Claude auf falschem Kontext arbeitet und falsche Entscheidungen trifft.

**Warum:** Diese Dateien sind Claudes primäre Informationsquelle beim Gesprächsstart. Stimmt der Inhalt nicht mit der Realität überein, entstehen Folgefehler — falsche Priorisierungen, redundante Arbeit, oder Vorschläge die am aktuellen Stand vorbeigehen. Regelmäßiges Abgleichen (z.B. beim Workflow-Checkpoint) ist essentiell.

### Kontext-Qualität vor Quantität
**Erkenntnis:** Der Agent ist nur so gut wie der Kontext, den wir ihm geben. Gleichzeitig geht es nicht um Quantität, sondern um Qualität und Aktualität. Deswegen ist es wichtig, die Informations- und Kontextdateien aktuell zu halten und in einer für AI optimalen Größe zu pflegen.

**Warum:** Zu viel Kontext verwässert die relevanten Informationen — zu wenig oder veralteter Kontext führt zu falschen Annahmen. Die Kunst liegt darin, dem Agenten genau das zu geben, was er braucht: aktuell, kompakt und präzise.

### Klein anfangen statt Framework-Overkill
**Erkenntnis:** Da draußen gibt es jede Menge Frameworks, die zwar alles abdecken und sexy aussehen, aber letztendlich selten wirklich produktiv eingesetzt werden. Zu komplex, Lernkurve zu steil, unübersichtlich.

Deswegen habe ich angefangen, mit einzelnen Schritten zu arbeiten, die mich tatsächlich bei der Arbeit unterstützen — und so meinen Workflow Stück für Stück aufzubauen. Das kann jeder für sich bauen oder einzelne Schritte übernehmen.

**Warum es sich lohnt:** Das ist ein schneller Weg zur Automatisierung aller Routinen, die tatsächlich automatisch oder zumindest halbautomatisch ablaufen können. Kein theoretisches Framework-Studium nötig — einfach anfangen, was funktioniert behalten, was nicht passt anpassen.

### Agent-Teams: Drei fokussierte Perspektiven
**Kontext:** Beim Design von `/dtb:plan-review` habe ich mir das BMAD-Framework angeschaut — dort gibt es 5 Rollen (Bob, Alice, Charlie, Dana, Elena). Das ist für ein Solo-Projekt nicht realistisch: kein QA-Team, keine Junior-Devs, kein Scrum-Master nötig. Aber drei fokussierte Perspektiven decken die relevanten Aspekte eines Implementierungsplan-Reviews ab.

**Rollenaufteilung die funktioniert:**

| Rolle | Warum | Was sie tut |
|-------|-------|-------------|
| Architekt | Prüft ob der Plan systemisch solide ist | Abhängigkeiten, Risiken, Systemgrenzen, Edge Cases |
| Pragmatiker | Hält den Scope realistisch | "Zu groß", "Phase 2 reicht erstmal", MVP-Schnitt |
| Senior Dev | Prüft die technische Umsetzbarkeit | Realistische Zeitschätzungen, Teststrategie, fehlende Migrationen/Schritte auf Code-Ebene |
| Du (Damian) | Entscheidungshoheit + Domain-Wissen | Wirst gefragt, gibst Kontext, entscheidest |

**Kerngedanke:** Damian ist nicht ein weiterer Agent — er ist der Product Owner. Die Agenten diskutieren, stellen gezielt Fragen ("Damian, brauchst du Feature X wirklich in Phase 1?"), und er entscheidet. Ein Koordinator/Scrum-Master ist bei 3 Agenten + PO unnötig — das wäre Over-Engineering.

**Warum drei und nicht zwei:** Der Senior Dev ist kein Koordinator, sondern bringt eine eigenständige Perspektive: die Code-Level-Machbarkeit. Architekt denkt in Systemen, Pragmatiker denkt in Scope — aber keiner prüft ob die Schritte im Plan tatsächlich so umsetzbar sind, ob Zeitschätzungen realistisch sind, oder ob eine Teststrategie fehlt. Diese Lücke schließt der Senior Dev.

**Prinzip:** Jede Rolle muss eine eigene, nicht-redundante Perspektive haben. Keine Rolle "zur Sicherheit" — nur Rollen die eine echte Lücke schließen.

### Skills statt Commands — eine Variante reichen lassen
**Erkenntnis:** Wir hatten Commands und Skills parallel gepflegt — identischer Inhalt, doppelte Arbeit. Skills können alles was Commands können, plus Trigger-basierte Erkennung durch YAML-Frontmatter. Die Commands boten keinen Mehrwert.

**Warum:** Doppelpflege führt unweigerlich zu Drift. Wenn zwei Dateien denselben Inhalt haben, wird eine irgendwann veraltet sein. Lieber eine Single Source of Truth wählen und konsequent dabei bleiben. Skills sind die mächtigere Variante — Commands wurden entfernt.

### Ideen sofort einfangen, später ausarbeiten
**Erkenntnis:** Während der Arbeit kommen ständig Gedanken und Ideen. Ohne einen schnellen Weg sie festzuhalten, gehen sie verloren oder unterbrechen den Flow. Die Lösung: `/dtb:idea` für sofortiges Erfassen (Freitext, keine Rückfragen), `/dtb:idea-review` für späteres Sichten, und `/dtb:feature-plan` greift offene Ideen automatisch auf.

**Warum:** Der Schlüssel ist die Trennung von Erfassen und Ausarbeiten. Beim Erfassen zählt Geschwindigkeit — kein Formular, keine Kategorisierung, kein Workflow. Die Struktur kommt später, wenn man bewusst Zeit dafür nimmt. So bleibt der aktuelle Arbeitsfluss ungestört.

### Kleine Funktionen bauen statt jedes Mal von vorne beschreiben
**Erkenntnis:** Es lohnt sich, in kleinen wiederverwendbaren Funktionen zu denken — anstatt jedes Mal ausführlich und manuell von Neuem zu beschreiben, was passieren soll, lieber ein kleines System bauen, das eine Funktionalität abbildet. Skills sind genau das: kompakte, wiederverwendbare Bausteine für wiederkehrende Aufgaben.

**Der springende Punkt:** Mit Claude als Arbeitsbuddy geht das einfach und schnell. Man beschreibt einmal, was man braucht, und hat in Minuten einen funktionierenden Skill. Kein aufwändiges Framework-Design, kein Boilerplate — einfach bauen, testen, nutzen.

**Für andere:** Wer sich das claude-code-workflow-kit runterlädt, wird feststellen: Claude versteht die Struktur sofort — und genauso dein Projekt. Claude beurteilt, was zu deiner Arbeitsweise passt und was nicht, nimmt dich an die Hand und zeigt, wo die Skills gleich einen Mehrwert liefern und wo man sie an deine Arbeitsweise anpassen sollte. Der Einstieg ist nicht "lies die Doku", sondern "starte Claude und lass dir zeigen, was für dich funktioniert".

### Implizites Wissen explizit und maschinenlesbar machen
**Erkenntnis:** Die Pipeline zwischen den Skills war immer schon da — verteilt über Freitext in "Nächste Schritte" und "Verwandte Commands". Aber kein Skill wusste maschinell, wo er in der Kette steht, was er konsumiert oder produziert. Durch das Pipeline-Frontmatter (`after`, `next`, `consumes`, `produces`) wird aus implizitem Wissen strukturierte Daten, die Tools wie `project-health` automatisch validieren können.

**Prinzip:** Wenn etwas eine Struktur hat, sollte es auch als Struktur abgebildet sein — nicht als Prosa. Prosa ist für Menschen gut lesbar, aber ein Tool kann damit nichts anfangen. Strukturierte Metadaten ermöglichen automatische Konsistenzprüfungen, Visualisierungen und Fehlererkennung — Dinge, die bei Prosa manuell passieren müssten.

**Konkretes Beispiel:** Vorher stand in einem Skill "Nächster Schritt: /dtb:impl-plan". Jetzt steht im Frontmatter `next: dtb:impl-plan` — und `project-health` kann prüfen, ob dieser Skill tatsächlich existiert, ob die Rückrichtung stimmt, und ob es zirkuläre Referenzen gibt. Gleicher Inhalt, aber maschinenlesbar.

### Sub-CLAUDE.md als kontextuelle Doku-Schichten
**Erkenntnis:** Die Root-CLAUDE.md wird bei jeder Conversation geladen und sollte deshalb schlank bleiben (<150 Zeilen). Aber bereichsspezifische Konventionen müssen trotzdem irgendwo dokumentiert sein — z.B. wie man einen neuen Skill schreibt oder wie Agent-Dateien strukturiert sein müssen.

**Lösung:** Sub-CLAUDE.md Dateien in Unterverzeichnissen (`skills/CLAUDE.md`, `agents/CLAUDE.md`). Diese werden nur geladen, wenn Claude in dem jeweiligen Verzeichnis arbeitet. So bekommt der Agent die richtigen Regeln genau dann, wenn er sie braucht — ohne die Root-Datei aufzublähen.

**Warum das funktioniert:** Claude Code lädt CLAUDE.md Dateien kontextabhängig — die Root-Datei immer, Sub-Dateien nur wenn im entsprechenden Verzeichnis gearbeitet wird. Das ist ein natürlicher Mechanismus für geschichtete Dokumentation: allgemeine Regeln oben, spezifische Details dort wo sie gebraucht werden.

### Für die AI denken, nicht für Menschen dokumentieren
**Erkenntnis:** Beim Erstellen von Skills, Rules und Kontext-Dateien ist die entscheidende Frage nicht "Wie würde ein Mensch das lesen?", sondern "Was braucht die AI, um optimal zu arbeiten?". Das bedeutet: keine ausführlichen Manuals oder Erklärungstexte, sondern schmale, gezielte Informationen — kompakt, strukturiert, direkt umsetzbar.

**Warum:** Die AI liest keine Doku zum Verständnis — sie braucht klare Anweisungen, Regeln und Kontext um Entscheidungen zu treffen. Lange Erklärungen verwässern den Fokus, kurze Regeln mit Begründung sind sofort anwendbar. Ein "Do: X, weil Y" ist für die AI wertvoller als drei Absätze Hintergrund.

**Konkret:** Rules-Dateien in `project-rules/` sollten keine Coding-Handbücher sein, sondern knappe Checklisten: Was gilt, warum, und ein Beispiel-Pfad. Dasselbe Prinzip gilt für CLAUDE.md, Memory-Dateien und Skill-Templates — immer fragen: "Ist das für die AI nützlich oder nur für menschliche Leser hübsch?"

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
