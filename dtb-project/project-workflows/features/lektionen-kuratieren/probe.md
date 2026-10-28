# Probe: Lektionen kuratieren

**Erstellt:** 2026-10-28
**Zweck:** Pruef- und Probe-Ablage des Changes (status-neutral, zaehlt fuer keine Ableitung).
Schritt 1.3: Voranalyse read-only am vollen Bestand, Uebersicht und Vorlagen in Zielform —
geschrieben wurde nichts an `lessons.md`.

---

## Probe 1.3 (2026-10-28)

**Lauf:** Repo-Fassung `skills/dtb-lesson-curate/SKILL.md`, 6 Explore-Agenten parallel
(Portionen nach Nummer: 1–15 · 16–21+35–43 · 44–58 · 59–73 · 74–88 · 89–100).

**Abweichung vom Plan (Mensch: „anpassen und fortfahren"):** Der Auftrag traegt nur noch die
Nummern der Portion, der Agent liest `lessons.md` selbst. Grund: Zeilen + Gesamtliste je Auftrag
haetten ~115 KB Auftragstext ergeben (Bestand 55 KB), und die Dubletten-Pruefung haette nur
~100 Zeichen der anderen Lektionen gesehen. Skill-Schritt 2b entsprechend angepasst.

### Uebersicht (Zielform)

```
Lektionen kuratieren — Bestand 87 Lektionen, 96 Zeilen, 54 KB (Schwelle 40 KB)

Voranalyse: 87 geprueft · 0 nicht geprueft
  Vorschlaege: 5 (ueberholt 3 · gehoben 2 · doppelt 0)
  davon Sammelliste: 1 · Einzelfaelle: 4 · gekappt: 0
  Erwartete Einsparung bei voller Annahme: 3 KB → 51 KB (bleibt ueber der Schwelle)
```

### Muster-Sammelliste (Zielform)

```
Sammelliste — 1 Lektion, Wirkung je Zeile: → Archiv (archive/lessons-ausgemustert.md)

 1. L8  gehoben   Negativ-Kriterien auf die Wirkstelle ankern — skills/CLAUDE.md traegt
                  dieselbe Regel mit demselben Praxisfall        skills/CLAUDE.md:630-641  → Archiv
```
Knopf: **Alle uebernehmen (Vorschlag)** · Nummern streichen · Einzeln durchgehen

### Muster-Einzelfaelle (Zielform)

Alle vier mit Sicherheit `mittel` → Einzelfall (Regel aus Plan 2.1: Sammelliste nur `hoch` +
Beleg-Ort). 4 ≤ `einzeln_pro_lauf` 5 → keine Kappung.

```
Einzelfall 1/4 — L1 (2026-07-15) · Vorschlag: ueberholt (mittel)
  Rule: Bei Phasen-Kriterien „verletzt" (pruefbar rot bzgl. bereits umgesetzter Schritte) von
        „ausstehend" (liefert ein spaeterer Schritt) trennen — nur Verletzung blockiert,
        Ausstehendes nicht
  Grund: dtb:implement unterscheidet bei der Flip-Bedingung inzwischen selbst zwischen
         „verletzt" und „ausstehend".
  Beleg: skills/dtb-implement/SKILL.md:102-106
```
Knopf: **Ausmustern (ueberholt)** · Behalten

```
Einzelfall 2/4 — L4 (2026-07-18) · Vorschlag: ueberholt (mittel)
  Rule: `implement` liest `lessons.md` bewusst als Prior (wie impl-plan/plan-review/code-review)
        — Sektion + `consumes`-Eintrag sind Absicht, kein Drift; …
  Grund: Steht inzwischen fest im Frontmatter, in einer eigenen Sektion und im Kopf der Sammlung.
  Beleg: skills/dtb-implement/SKILL.md:16, :32-41; dtb-project/project-rules/lessons.md:4
```
Knopf: **Ausmustern (ueberholt)** · Behalten

```
Einzelfall 3/4 — L10 (2026-08-06) · Vorschlag: gehoben (mittel)
  Rule: Unscharfe Schwellen als Ersetzungsprobe formulieren statt als Quote, plus asymmetrische
        Tie-break-Regel fuer den Zweifelsfall — …
  Grund: skills/CLAUDE.md traegt die Ersetzungsprobe samt Begruendung und Zweifelsregel; die
         Lektion fasst den Gegenstand etwas allgemeiner („jede unscharfe Schwelle").
  Beleg: skills/CLAUDE.md:152-172
```
Knopf: **Ausmustern (gehoben)** · Behalten

```
Einzelfall 4/4 — L84 (2026-09-30) · Vorschlag: ueberholt (mittel) · Applies-to: alle
  Rule: `blocked` im Tick als Wartezustand behandeln: den Dialog per `herdr pane read` zeigen
        und auf den Menschen verweisen, nicht als Stoerung melden
  Grund: Der Ueberwachungs-Tick in dtb:worker behandelt `blocked` schon selbst so; fuer
         Ueberwachung ausserhalb des Ticks koennte die Lektion noch gelten.
  Beleg: skills/dtb-worker/SKILL.md:303, :374, :419-420
```
Knopf: **Ausmustern (ueberholt)** · Behalten

### Zaehlung (Mengenprobe, L90)

Zaehlung behalten: 82
Zaehlung ueberholt: 3
Zaehlung doppelt: 0
Zaehlung gehoben: 2
Zaehlung nicht geprueft: 0

Summe = 87 = Anzahl Lektionen (`LEKTIONEN 87` aus Schritt 1a). Gate 2c: alle 6 Portionen
Nummern-Gate OK, 0 Spalten-/Urteils-Ausreisser.

### Befunde fuer die Abnahme

- **Ausbeute gering:** 5 von 87 Vorschlaegen, ~3 KB. Die Sammlung bliebe bei 51 KB und damit
  ueber der 40-KB-Schwelle — die Warnung feuert auch nach voller Annahme weiter. Hauptgrund laut
  Agenten-Begruendungen: viele Lektionen tragen eine *allgemeine* Regel, die Skills nur lokal
  anwenden; Hebe-Ziel ist allein `skills/CLAUDE.md` (keine weiteren Regel-Dateien in
  `project-rules/`).
- **Grenzfall:** L41 als `behalten (niedrig)` mit Hinweis „nahe ueberholt" — bleibt nach Regel
  ohne Vorschlag (im Zweifel behalten).
- **Teil-Hebungen:** L7 und L94 werden als „nur zum Teil gehoben" behalten — die
  Ersetzungsprobe greift wie vorgesehen.
- **Werkzeug-Hinweis (L7):** Ein erster Spalten-Check mit `sed 's/\|//g'` zerlegte drei Zeilen
  mit `\|\|` falsch (GNU-sed-BRE); mit `sed 's/[\][|]//g'` alle sauber. Kein Datenbefund — fuer
  Phase 2 vormerken: escapte Pipes per Klammer-Ausdruck entfernen.

### Rohzeilen der Agenten

```
L1 | ueberholt | dtb:implement unterscheidet bei der Flip-Bedingung inzwischen selbst zwischen „verletzt“ und „ausstehend“, sodass sich das Phasen-Gate nicht mehr selbst blockieren kann. | skills/dtb-implement/SKILL.md:102-106 | mittel
L2 | behalten | Die Regel gilt für jeden Verifikations-Grep, der auf ein bloßes Stichwort zielt (Fehltreffer durch Doku-Zitate); L8 und skills/CLAUDE.md:630 decken nur den schmaleren Fall der Negativ-Kriterien ab. | — | hoch
L3 | behalten | Vor einem Skill-Umbau repo-weit nach dem Skill-Namen zu greppen, schreibt weder ein Skill noch skills/CLAUDE.md vor; L44 betrifft nur consumes/produces. | — | hoch
L4 | ueberholt | Dass implement lessons.md liest, steht inzwischen fest im Frontmatter, in einer eigenen Sektion und im Kopf der Sammlung, also kann es niemand mehr als ungeplanten Drift lesen. | skills/dtb-implement/SKILL.md:16 (consumes lessons.md), :32-41 (Sektion „Lektionen als Prior lesen“); dtb-project/project-rules/lessons.md:4 | mittel
L5 | behalten | impl-plan wertet einen fehlenden Pfad weiterhin pauschal als „veraltet“ und startet den Scan, ohne Neubau-Ziele auszunehmen; der Fehler ist also weiter möglich. | — | hoch
L6 | behalten | commit-and-push schreibt nach wie vor bewusst keine SHA zurück, und impl-review meldet SHA-lose Zeilen; das manuelle Nachtragen verlangt kein Skill. | — | hoch
L7 | behalten | skills/CLAUDE.md:619-628 trägt nur die Teile „Werkzeug-Fehlschlag ist kein Datenbefund“ und „Sequenz nicht ersetzen“; „Shell-Syntax nie über Werkzeuggrenzen mischen“ steht dort nicht, die Lektion ist also nur zum Teil gehoben. | — | mittel
L8 | gehoben | skills/CLAUDE.md trägt dieselbe Regel (Negativ-Kriterien auf die Wirkstelle statt auf die ganze Datei ankern) mit Begründung und demselben Praxisfall plan-status-feld. | skills/CLAUDE.md:630-641 | hoch
L9 | behalten | workflow-checkpoint erwähnt die Kette nur in einer Klammer; dass der Aufrufer kein Skill-Tool in allowed-tools braucht und wie man einen Auslöser verankert, steht nirgends, und L69/L77 behandeln andere Aussagen. | — | mittel
L10 | gehoben | skills/CLAUDE.md trägt die Ersetzungsprobe statt einer Prozent-Quote mit derselben Begründung und dazu die asymmetrische Zweifelsregel; die Lektion fasst den Gegenstand etwas allgemeiner („jede unscharfe Schwelle“). | skills/CLAUDE.md:152-172 | mittel
L11 | behalten | Nur dtb:no-loss-check trägt die Regel, und zwar lokal; als allgemeine Regel für alle („nur git check-ignore, sonst feste Zuordnung“) steht sie nicht im Hebe-Ziel, auch wenn das lessons.md-Beispiel seit der Versionierung veraltet ist. | — | mittel
L12 | behalten | Die Nachbarschafts-Regel in skills/CLAUDE.md:585-593 gilt nur für Datei-Erzeugung; die Ausweitung auf Triage-Fixes und die Prüfung der Naht zwischen gekoppelten Findings fehlen dort und in der impl-review-Triage (Schritt 9). | — | hoch
L13 | behalten | Die Triage in impl-review (Schritt 9) führt nach Fixes die Automated-Kriterien der betroffenen Phasen nicht erneut aus, und L12 deckt den Fall über Dateigrenzen ausdrücklich nicht ab. | — | hoch
L14 | behalten | Dass Kalibrierung an einem Fall-Set und Text-Review verschiedene Fehlerklassen finden, steht weder in skills/CLAUDE.md noch in einem Skill. | — | hoch
L15 | behalten | Die Pflicht, den eigenen neuen Text gegen genau die beseitigte Fehlerklasse zu prüfen, steht nirgends; L16 betrifft die Prüffrage einer Gegenprobe und damit eine andere Aussage. | — | hoch
L16 | behalten | Die Regel, die Prüffrage vor einer Gegenprobe ausdrücklich zu formulieren, steht in keinem Skill und in skills/CLAUDE.md nicht; L15 und L12 haben einen anderen Gegenstand. | — | hoch
L17 | behalten | Nur die Nummernvergabe in skills/dtb-idea/SKILL.md:152 und skills/dtb-idea-triage/SKILL.md:802 wendet die Stichprobe an; die allgemeine Regel für jede gemeldete Bestandszahl und das Verbot, Statuskategorien zu verrechnen, stehen nirgends sonst. | — | hoch
L18 | behalten | Der Pane-Träger prüft die Auftragsdatei (skills/dtb-worker/SKILL.md:245, skills/dtb-pane-start/SKILL.md:166), der Subagenten-Träger aber weiterhin nur die vom Task berührten Pfade (skills/dtb-worker/SKILL.md:522-523) — genau die Lücke der Lektion. | — | mittel
L19 | behalten | skills/dtb-task/SKILL.md:200 setzt eine geroutete Idee unbedingt auf `Ausgearbeitet` und kennt kein Teil-Routing; die Regel trägt also noch und steht nirgends sonst. | — | hoch
L20 | behalten | Die Pflicht zu einem Ablageort für Plan-Schritte ohne Datei-Ergebnis fehlt in impl-plan, plan-review und skills/CLAUDE.md (`Ablageort` 0 Treffer in skills/). | — | hoch
L21 | behalten | Die Regel, ortsgebundene Verifikationsschritte zu zerlegen und den ortsunabhängigen Teil sofort lokal zu belegen, steht in keinem Skill und in keiner anderen Lektion. | — | hoch
L35 | behalten | Der sync-Modus von kit-sync schreibt das Lock (skills/dtb-kit-sync/SKILL.md:235-236), liest aber nichts als unabhängigen Zeugen zurück (mtime, `updatedAt`/`sourceCommit`); L7 und Mechanik-Regel CLAUDE.md:619 fordern nur gefüllte Vergleichsseiten, nicht die Identität mit dem Schreibziel. | — | hoch
L36 | behalten | Die quoting-feste CR-Prüfung (awk statt `$'\r'` in verschachtelter Kommandosubstitution) steht nirgends sonst; L80 betrifft CRLF in Python-Ausgabe, eine andere Aussage. | — | hoch
L37 | behalten | Die Regel, vor dem ersten Pull nach einer .gitignore-Negation die lokale Kopie zu sichern, ist allgemein und steht nirgends sonst; L11 betrifft nur, wie man den Ignorier-Status ermittelt. | — | mittel
L38 | behalten | L91 schärft L38 nur für kurze Regex- und Python-Logik, L100 nur für Merge-Nachrichten; L38 bringt mehr mit (lange Inhalte mit Unicode und Backticks, `git commit -F`) und wird von keiner der beiden ersetzt. | — | hoch
L39 | behalten | kit-sync klont die Quelle (skills/dtb-kit-sync/SKILL.md:101-106), prüft aber nicht, ob der Branch ahead ist (`ahead` 0 Treffer in skills/dtb-kit-sync/); die Regel wird also nicht erzwungen. | — | hoch
L40 | behalten | Der Fehler mit `~`-Pfaden von Bash an Windows-Python steht in keinem Skill (`expanduser` 0 Treffer in skills/) und in keiner anderen Lektion. | — | hoch
L41 | behalten | skills/dtb-workflow-checkpoint/SKILL.md:553 trägt dieselbe Aussage nur als Antwortregel für das Modell; die Vorlagenzeile für den Menschen (:546) erklärt das nicht, der Fehler bleibt also möglich, und Skill-Dateien sind kein Hebe-Ziel — Grenzfall nahe ueberholt. | — | niedrig
L42 | behalten | Die Regel, bei erweitertem Eingang Bedingung und Zählgröße des Wächters mitzuziehen, steht nirgends sonst; L47 (neue Zählgröße) und die Nachbarschafts-Regel in CLAUDE.md:585 haben andere Aussagen. | — | hoch
L43 | behalten | Nur skills/dtb-idea-triage/SKILL.md:571 wendet „Ziel vor Quelle“ für einen Fall an; die allgemeine Regel für Beförderung, Archivierung und Migration steht weder in skills/CLAUDE.md noch in einer anderen Lektion. | — | hoch
L44 | behalten | Die Pflicht, consumes/produces im selben Zug mit dem Datei-Umgang nachzuziehen, steht weder in skills/CLAUDE.md (dort nur die Feld-Definition, Z.18-19/38-39) noch wird sie erzwungen: der project-health-Lint vergleicht Frontmatter nur mit anderem Frontmatter, nicht mit dem Fliesstext (skills/dtb-project-health/SKILL.md:223). | — | hoch
L45 | behalten | Die Regel, einen von mehreren Skills geteilten Zaehlbegriff einmal an der Datenquelle festzuschreiben, steht nirgends; skills/CLAUDE.md:43-45 macht nur DERIVED_STATE_RULES zur einzigen Quelle fuer Status-Ableitungen, also schmaler und ein anderer Gegenstand. | — | mittel
L46 | behalten | Nur dtb-idea-triage fuehrt die Referenz-mtime nach eigenem Schreiben nach (skills/dtb-idea-triage/SKILL.md:157-158). dtb-idea-review prueft vor JEDER Statusentscheidung und fuehrt die mtime nicht nach (skills/dtb-idea-review/SKILL.md:84-96), dort tritt der Fehler also weiter auf; der Kanon skills/CLAUDE.md:538-548 enthaelt die Regel ebenfalls nicht. | — | hoch
L47 | behalten | Eine eingefuehrte neue Zaehlgroesse zwingt dazu, die alte an allen Fundstellen neu zu definieren; das ist eine eigene Aussage, die weder L42 (Waechter bei erweitertem Eingang) noch L45 (gemeinsame Definition an der Quelle) noch skills/CLAUDE.md abdeckt. | — | hoch
L48 | behalten | Der Umweltfall (AVG/TLS-Proxy, certifi fest verdrahtet) steht sonst nirgends; L88 verweist sogar auf diese Lektion als Quelle. | — | hoch
L49 | behalten | Die Kodierungs-Falle von PowerShell 5.1 (BOM-lose Dateien als ANSI, `.ps1` mit BOM) steht weder in skills/CLAUDE.md noch in einer anderen Lektion. | — | hoch
L50 | behalten | Der Tipp MediaPlayer statt WMPlayer-COM betrifft ein Werkzeug ausserhalb der Skills und steht sonst nirgends; ob es den Hook noch gibt, ist in diesem Repo nicht pruefbar. | — | mittel
L51 | behalten | Es geht um Testdaten mit Backslashes als Datei; L66 nennt sich selbst nur „verwandt“ (Konfigurationsdatei), und L91 deckt Skript-Logik ab, nicht Test-Eingabedaten. | — | hoch
L52 | behalten | Hintergrund-Prozesse per PID statt per Image-Name beenden, dazu steht nichts in skills/CLAUDE.md und in keiner anderen Lektion. | — | hoch
L53 | behalten | skills/CLAUDE.md:624 und L7 verbieten zwar, eigene Hash-/Grep-Methoden statt der vorgegebenen Sequenz zu nutzen, aber nicht so konkret: die Klassen-Muster woertlich uebernehmen (agents/*.md schliesst agents/CLAUDE.md ein), keine Ausnahmen aus anderen Skills einbauen, und ein „verwaist“ gegen einen Lock-Eintrag zuerst als Werkzeugfehler pruefen; dtb-kit-sync erzwingt das nicht. | — | mittel
L54 | behalten | Die Regel, globale Artefakte (Startmenue, Registry, PATH) nur anzufassen, wenn sie nachweislich zur eigenen Installation gehoeren, und Wegwerf-Tests mit Schaltern gegen globale Effekte zu fahren, steht sonst nirgends. | — | hoch
L55 | behalten | Die Fallen bei `irm \| iex` (`exit` schliesst das Fenster, Aufrufer-Scope wird veraendert, BOM, keine Parameter) stehen weder in skills/CLAUDE.md noch in einer anderen Lektion. | — | hoch
L56 | behalten | Eine Wirklauf-Anleitung muss mindestens eine Entscheidung vorgeben, die tatsaechlich schreibt; das deckt L74 (Repo-Fassung statt installierter Kopie) nicht ab, und ein Skill erzwingt es nicht. | — | hoch
L57 | behalten | Manual-Kriterien nur an Objekte binden, die der Abnahme-Lauf selbst erzeugt: dazu gibt es in skills/ keine Regel („Wegwerf“/„Bestands-Item“ 0 Treffer in skills/), und keine andere Lektion traegt die Aussage. | — | hoch
L58 | behalten | Ein vom Auto-Modus abgelehntes Loeschen nicht auf anderem Weg ausfuehren: L81 behandelt mit Plugin-Installation einen anderen Gegenstand und laesst den Teil zum Umgehungsverbot und zur Permission-Regel weg. | — | hoch
L59 | behalten | Die Pflicht, einen `## Rueckweg` bei der Abnahme gegen `git log` zu pruefen, SHA-Platzhalter aufzuloesen und bei Fremdanteilen pfadgezielt zurueckzudrehen, steht weder in einem Skill noch in skills/CLAUDE.md (`Rueckweg` trifft dort nur den Hand-off-Rueckweg von Panes). | — | hoch
L60 | behalten | Die Regel zu nummernbasiertem `sed -i` nach Loeschungen in derselben Datei steht nirgends sonst (`sed -i` 0 Treffer in skills/), und keine andere Lektion behandelt veraltete Zeilennummern. | — | hoch
L61 | behalten | `dtb:idea-rank` wendet die Grenze lokal an (skills/dtb-idea-rank/SKILL.md:163,171), die allgemeine Schreibregel fuer Plaene und Reviews („nie Ignorieren aus einer ungelesenen Quelle fordern“) traegt aber nur diese Lektion. | — | mittel
L62 | behalten | dtb:impl-review sieht keinen Folgelauf nach einer Triage mit strukturellen Fixes vor; L13 verlangt nur, die Automated-Kriterien erneut auszufuehren, L65 regelt nur das Ende der Folgelaeufe – beide haben eine andere Aussage. | — | hoch
L63 | behalten | Die feste Quell-Sequenz in kit-sync nutzt `git -C`, kettet `git clone` aber nicht mit `\|\| exit 1` (skills/dtb-kit-sync/SKILL.md:104); die allgemeine Abbruchregel fuer Beschaffung und `cd` steht in keiner Hebe-Datei, und L100 betrifft nur Merge und Push. | — | mittel
L64 | behalten | Eine Beispiel-Ausgabe in Zielform als Manual-Gate in Phase 1 bei Report- und Sicht-Skills ist weder in dtb:impl-plan noch in skills/CLAUDE.md verankert (`Beispiel-Ausgabe`/`Zielform` 0 Treffer in skills/); L14 hat eine andere Aussage. | — | hoch
L65 | behalten | Das Abbruchkriterium „Folgelaeufe nach Schwere statt nach Anzahl beenden“ steht nirgends sonst und ergaenzt L62, statt es zu wiederholen. | — | hoch
L66 | behalten | JSON-Konfigurationen parsen statt per Heredoc oder Textersatz zu schreiben, inklusive Parse-Verifikation und Hinweis auf stillen Settings-Verlust, geht ueber L51 (nur Testdaten) und L38 (nur lange Heredocs) hinaus. | — | hoch
L67 | behalten | Dass `/clear` keine neu gelesenen Settings und keine neue Skill-Liste bringt, steht nur hier; L73 grenzt sich ausdruecklich davon ab und verweist auf L67. | — | hoch
L68 | behalten | Die Regel zu gepasteter Hersteller-Copy mit Injektionsmuster (erst lesen, Marketplace-Registrierung benennen, Mensch entscheiden) ist breiter als L81 (Classifier-Block, Zeilen zum Selbstausfuehren) und L72 (Abruf ueber WebFetch). | — | hoch
L69 | behalten | Die Regel zum Ausfuehren eines menschlich abgesetzten Slash-Befehls ohne `command-name`-Block steht in keinem Skill (`command-name` 0 Treffer in skills/); L77 schraenkt sie nur fuer Hand-offs ein, L9 betrifft einen anderen Fall. | — | hoch
L70 | behalten | Die Selbst-Eskalation von feature-fast deckt nur den Teil „mehr als 2 Phasen“ ab (skills/dtb-feature-fast/SKILL.md:162-167); das Kriterium Mitrede-Bedarf bei der Lane-Wahl steht nirgends (`Mitrede` 0 Treffer in skills/). | — | mittel
L71 | behalten | Die Rueckfuehrung von Secrets in den Verlauf ueber die Meldung „file changed on disk“ und der Umgang damit (Umgebungsvariable, Vorab-Hinweis, Rotation) sind nirgends sonst festgehalten. | — | hoch
L72 | behalten | Dass Injektion auch beim Abruf ueber WebFetch wirkt, samt Prompt-Zusatz und Vorzug fuer API-Referenzseiten, steht nur hier (`WebFetch` 0 Treffer in skills/); L68 behandelt den Paste-Pfad. | — | hoch
L73 | behalten | Dass Env-Aenderungen in den Settings sofort wirken und kein Neustart noetig ist, steht nur hier und ergaenzt L67, ohne es zu wiederholen. | — | hoch
L74 | behalten | Die Regel gilt allgemein: Probeläufe geänderter Skills laufen gegen die Repo-Fassung. Steht nirgends sonst, workflow-checkpoint (Struktur-Check, Repo zuerst) wendet das Prinzip nur für einen einzelnen Fall an. | — | hoch
L75 | behalten | In impl-plan, plan-review und impl-review steht keine Pflicht, beim Einführen neuer Kommandos `allowed-tools` zu prüfen. skills/CLAUDE.md:28 beschreibt nur das Feld. | — | hoch
L76 | behalten | `Beispielausgabe` und `Zielform` haben 0 Treffer in skills/. L64 verlangt nur, die Zielform abnehmen zu lassen, nicht Nachschärfungen dagegen gegenzulesen. | — | hoch
L77 | behalten | Die Rückweg-Anweisung in pane-start verweist nicht mehr auf L69. Die eigentliche Regel fehlt aber überall: Eine Checkpoint-Aufforderung aus einem Hand-off führt der Orchestrator nicht aus, der Mensch tippt den Befehl. | — | mittel
L78 | behalten | Jev und TypeSafe sind weiter Thema (INBOX #99 offen). Die Regel, den `state` gezielt zusammenzustellen, steht in keinem Skill und in keiner Hebe-Ziel-Datei. | — | hoch
L79 | behalten | Der Tick schlägt jetzt einen 15-Minuten-Takt vor, nennt aber keinen Hinweis auf die Eingabezeile einer wartenden Pane (`Eingabezeile` 0 Treffer in skills/). Der Kern der Lektion ist damit nicht getragen. | — | hoch
L80 | behalten | `tr -d '\r'` kommt in skills/ nur beim Datei-Hashing und bei Anker-Greps vor, nie für Python-Ausgabe, die Bash zeilenweise liest. L36 behandelt CR-Grep, das ist eine andere Aussage. | — | hoch
L81 | behalten | Gleicher Gegenstand wie L68, aber mehr Inhalt: der Classifier blockt, dem Nutzer gleich die `! claude plugin`-Zeilen geben, danach per Datei prüfen. L68 deckt nur ab, gepastete Installationstexte nicht ungefragt auszuführen. | — | hoch
L82 | behalten | skills/CLAUDE.md nennt die Fakten (Klasse B wird nur einmal kopiert, Seeds erreichen Bestandsprojekte nicht) und wendet die Regel einmal an. Die allgemeine Vorschrift „Regeln für Bestandsprojekte gehören inline in Klasse-A-Skills“ steht dort nicht. | — | mittel
L83 | behalten | Die Prüfung, ob die Rückfrage im Skill wirklich gestellt wird, bevor man sie umbaut, steht in keinem Planungs- oder Review-Skill und nicht in skills/CLAUDE.md. | — | hoch
L84 | ueberholt | Der Überwachungs-Tick in dtb:worker behandelt `blocked` schon selbst als Wartezustand: Pane lesen, Dialog-Auszug zeigen, kein Eingriff, der Mensch entscheidet. Die Behandlung steht seit 2026-09-24. Für Überwachung außerhalb des Ticks könnte die Lektion noch gelten. | skills/dtb-worker/SKILL.md:374; skills/dtb-worker/SKILL.md:303; skills/dtb-worker/SKILL.md:419-420 | mittel
L85 | behalten | `merge-base` und `...HEAD` haben 0 Treffer in skills/. Die Branch-Verifikation in dtb:worker diffed sogar noch mit zwei Punkten gegen den laufenden Hauptbranch (`git diff --stat {default-branch}..task/{slug}`, skills/dtb-worker/SKILL.md:446). Die Lektion trägt also voll. | — | hoch
L86 | behalten | `send-text`, `\033` und `/config` haben 0 Treffer in skills/. Der Escape-Trick für das Einstellungsfenster steht nirgends sonst. | — | hoch
L87 | behalten | Die Start-Sequenz in dtb:worker (Erkennungs-Warten über `herdr pane list`) sagt nicht, wie der Status zu parsen ist. Die Warnung vor der Regex über ein flaches Objekt und die Pflicht, vor dem zweiten `pane run` roh nachzulesen, fehlen. | — | hoch
L88 | behalten | Betrifft das externe Projekt claude-code-tts, nicht skills/. Die Diagnose- und Update-Anweisung gilt weiter auf jedem Rechner. Ob alle Rechner inzwischen auf 7.3.1 sind, lässt sich hier nicht prüfen. | — | mittel
L89 | behalten | Die allgemeine Regel, den Struktur-Check vor die erste Nutzung (auch die lesende) zu legen, steht nirgends; skills/CLAUDE.md nennt nur die Position des Checks bei idea-triage (Schritt 4a) und fasst sie nicht als Regel. | — | hoch
L90 | behalten | Die Mengenprobe vor jeder Sammelvorlage (gezeigte Nummern = Eingangsmenge, Summe der Gruppen = N) steht weder in skills/CLAUDE.md noch in einem Skill (`Mengenprobe` 0 Treffer in skills/); L17 (Zaehlausdruck gegen Stichprobe pruefen) und L42 (Waechter bei erweitertem Eingang) haben einen anderen Gegenstand. | — | hoch
L91 | behalten | Die Lektion schaerft L38 auf kurze Regex-/Python-Einzeiler, die L38 ausdruecklich nicht erfasst; sie bringt also mehr mit als L38 bzw. L51 und ist nicht doppelt. | — | hoch
L92 | behalten | Die Wechselwirkung von `python -I` mit `PYTHONIOENCODING` steht nirgends sonst (`reconfigure` 0 Treffer in skills/, keine verwandte Lektion). | — | hoch
L93 | behalten | workflow-checkpoint setzt die Regel für einen Fall bereits um (Ableitung über `^Decision: PENDING`, nicht über das Gesamt-Verdikt; skills/dtb-workflow-checkpoint/SKILL.md:84-87, gespiegelt in skills/CLAUDE.md:350). Die allgemeine Regel für künftige Skill-Logik, die etwas aus review.md ableitet, ist aber nirgends gehoben. | — | mittel
L94 | behalten | workflow-checkpoint nutzt die eindeutige Endmarke und den Hinweis „ohne Einrückung“ bereits (skills/dtb-workflow-checkpoint/SKILL.md:103-117). Die allgemeine Schreibregel für Heredocs in Skill-Texten fehlt aber in skills/CLAUDE.md; dort steht nur die Multi-Root-Regel zu Heredoc-Varianten (Z. 610-614). | — | mittel
L95 | behalten | `MSYS_NO_PATHCONV` hat 0 Treffer in skills/, agents/ und commands/, und keine Lektion beschreibt die Pfadumwandlung von Slash-Befehlen. L40 betrifft die `~`-Expansion, also eine andere Aussage. | — | hoch
L96 | behalten | Dass mehrstufige Pane-Abnahmen vom Orchestrator per `herdr agent prompt` gefahren werden, steht nirgends; skills/CLAUDE.md:350 verweist nur auf denselben Abnahme-Lauf, um die Antwortform der Weiche zu begründen. | — | hoch
L97 | behalten | Die Regel, Befunde eines Abnahme-Laufs vor der Entscheidung „Abgenommen“ zuzuordnen, steht weder in skills/CLAUDE.md noch in einer anderen Lektion. | — | hoch
L98 | behalten | skills/CLAUDE.md:469 definiert den Voll-Guard als harten Abbruch, sagt aber nicht, dass man für Schritte hinter dem Guard kein eigenes Worktree-Verhalten spezifiziert. | — | hoch
L99 | behalten | project-dashboard hat den Read-Schritt zwischen Bash-Erzeugung und Edit bereits (skills/dtb-project-dashboard/SKILL.md:197-198). Die allgemeine Ablaufregel für andere Skills steht aber nirgends in skills/CLAUDE.md. | — | mittel
L100 | behalten | Dass `git merge -F -` nicht von stdin liest und der Push nur per `&&` an einen erfolgreichen Merge gekettet werden darf, steht nirgends. L63 (Kette mit `\|\| exit 1` bei kit-sync) und L38 (`git commit -F <datei>`) treffen nur Teilaspekte. | — | hoch
```

---

## Gegenprobe 3.3 (2026-10-28)

**Prueffrage (L16):** Traegt die Aussage nach der Aenderung noch? — nicht: steht der Name noch drin.
Jeder Treffer wurde gegen genau diese Frage bewertet.

### Alte Schwelle (`150 Zeilen\|~150\|/150`, ohne Changelog, Archiv und diesen Change-Ordner)

| Fundstelle | Bewertung |
|------------|-----------|
| `skills/dtb-project-init/SKILL.md:240` „schlank halten (<150 Zeilen)" | traegt — betrifft die Groesse der CLAUDE.md, nicht `lessons.md` |
| `WORKLOG.md:84` „schlank bleiben (<150 Zeilen)" | traegt — dieselbe CLAUDE.md-Aussage, historisch |

Die 8 Wirkstellen aus der Ist-Analyse (`lessons.md:6`, `dtb-lesson` ×3, `dtb-project-dashboard` ×4)
tragen keine Zeilen-Schwelle mehr.

### `append-only` im Lektionen-Kontext

| Fundstelle | Bewertung |
|------------|-----------|
| `dtb-lesson` Description, Einleitung, Sektionstitel `## Schritt 4: Append-only speichern` | traegt — `dtb:lesson` schreibt weiterhin nur anhaengend; der Titel ist Anker fuer Checkpoint und idea-triage, bleibt unveraendert |
| `dtb-lesson` Format-Regel „bestehende Zeilen garantiert unveraendert (append-only)" | traegt — gilt fuers Schreiben |
| `dtb-lesson` Richtlinie „Nie bestehende Eintraege aendern/loeschen" | traegt erst mit Zusatz — ergaenzt um „die Entnahme laeuft nur ueber `/dtb:lesson-curate`" |
| `dtb-lesson` Hebe-Hinweis „`lessons.md` bleibt die append-only Historie" | traegt — die Historie liegt jetzt verteilt auf `lessons.md` und Archiv, beide append-only beim Schreiben; kein Widerspruch |
| `dtb-lesson` Kopf-Template, `lessons.md:3-6` | neu formuliert, wortgleich |
| `dtb-idea-triage:325, :705`, `dtb-workflow-checkpoint:509, :561` | traegt — Verweise auf den unveraenderten Sektionsanker |
| `CLAUDE.md` (Knowledge management, Output Locations) | nachgezogen — Entnahme-Regel und Archiv genannt |
| `README.md:97` (`/dtb:lesson`) | traegt — beschreibt das Schreiben |

### `lesson-curate` (Erwartung: Skill, `dtb-lesson`, Dashboard, Doku)

Treffer in `skills/dtb-lesson-curate`, `skills/dtb-lesson` (Kopf-Template, Warnung, Kopplungs-Hinweis,
Richtlinie), `skills/dtb-project-dashboard` (Kuratierungs-Satz, Kopplungs-Hinweis),
`skills/dtb-project-init` (Config-Regel), `skills/CLAUDE.md` (Voll-Guard-Zeile, Zeile H),
`CLAUDE.md`, `README.md`, `lessons.md`-Kopf, `workflow.config.yaml`. Keine Stelle verweist auf einen
nicht vorhandenen Abschnitt.

### Leser von `archive/` (Grep `archive/` ueber `skills/`)

Bewertet wurde, ob ein Leser lose Dateien in `archive/` deutet — nur dann trifft ihn
`archive/lessons-ausgemustert.md`:

| Leser | Bewertung |
|-------|-----------|
| `dtb:migrate-change-folders` (Schritt 1, Erkennung) | **trifft** — jede lose `.md` in `archive/` ausser `ARCHIVE_LOG.md` gilt als flaches Altlayout. Heute schon bei `INBOX-BEFUNDE-verworfen.md`, kuenftig auch bei `lessons-ausgemustert.md`: die Erkennung meldet „gemischt" statt „bereits migriert". Entscheidung 2026-10-27: NICHT hier reparieren → eigene Idee im Hand-off |
| `dtb:idea-triage` (Agenten-Suchraum `{wf}/archive/`) | traegt — liest nur als Kontext „umgesetzt, archiviert?"; ein Fund im Lektionen-Archiv waere sogar ein korrekter Hinweis |
| `dtb:project-health` (ARCHIVE_LOG, `archive/<slug>/`) | traegt — prueft Ordner, keine losen Dateien |
| `dtb:archive`, `implement`, `impl-review`, `idea-rank`, `workflow-*` | traegt — lesen nur `archive/{slug}/` bzw. `ARCHIVE_LOG.md` |

### Ergebnis

Keine Altstelle uebrig. Ein bekannter Folgefehler ausserhalb des Scopes (`dtb:migrate-change-folders`),
bereits als eigene Idee fuer den Orchestrator vorgemerkt.
