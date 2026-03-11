# Claude Code Memory Framework

Wzorce do efektywnego zarządzania pamięcią agenta AI w Claude Code - wypracowane w codziennym, produkcyjnym użyciu. Nie kolejny tutorial o `CLAUDE.md`, ale konkretne techniki, których brakuje w domyślnej konfiguracji.

> **[English version](README.en.md)**

## Co tu znajdziesz (a czego nie daje Ci Claude Code)

Claude Code ma wbudowany system pamięci - `CLAUDE.md`, katalog `memory/`, auto-ładowany `MEMORY.md`. To działa. Ale po kilku tygodniach intensywnej pracy pojawią się problemy, których domyślna konfiguracja nie rozwiązuje:

- Agent robi coś destrukcyjnego, bo "wydawało mu się" że może
- Pamięć rośnie, aż zostaje obcięta w połowie zdania
- Te same błędy techniczne powtarzają się co kilka sesji
- Agent zapisuje bieżące zadania zamiast trwałej wiedzy

Ten framework adresuje te problemy trzema wzorcami:

## 1. Model autonomii agenta

**Problem:** Claude Code ma ogólną zasadę "zapytaj przy ryzykownych akcjach", ale nie definiuje co jest ryzykowne w Twoim środowisku. Agent zgaduje - czasem trafia, czasem nie.

**Rozwiązanie:** Jawna taksonomia z czterema poziomami uprawnień.

```markdown
## WOLNO - bez potwierdzenia
- Czytanie plików, eksploracja kodu, uruchamianie testów
- Edycja lokalnych plików, tworzenie commitów (gdy poproszony)
- Aktualizacja plików pamięci
- Lokalne operacje git (status, diff, log, branch)

## ZA ZGODĄ - czekaj na jawne "tak" / "wyślij" / "pushuj"
- Wysyłka emaili i wiadomości
- Git push, tworzenie PR/issues
- Restart serwisów, deploy
- Cokolwiek co kosztuje pieniądze
- Destrukcyjny git (force push, reset --hard)
- Zmiany infrastruktury (firewall, SSL, DNS)

## NIGDY - bezwzględny zakaz, nawet jeśli użytkownik zapomni
- Sekrety w plikach pamięci lub commitach
- Kosztowne wywołania API bez zgody
- Destrukcyjne operacje jako skróty (usuwanie lockfile'ów, --no-verify)
- Pomijanie hooków bezpieczeństwa

## ESKALACJA - gdy nie wiadomo
Jeśli akcja nie pasuje jednoznacznie do WOLNO -> ZAPYTAJ.
Lepiej zapytać raz za dużo niż zrobić coś nieodwracalnego.
```

**Dlaczego to działa:** Agent stosuje się do jasnych, jawnych reguł. "NIGDY nie commituj .env" jest skuteczniejsze niż "bądź ostrożny z .env". Poziom ESKALACJA jest kluczowy - daje agentowi bezpieczną opcję "nie wiem, pytam" zamiast zgadywania.

**Jak dostosować:** Szablon w `templates/autonomy-rules.md` ma sekcję Customization. Dodaj reguły specyficzne dla swojego środowiska. Im więcej przypadków pokryjesz, tym rzadziej agent zgaduje.

## 2. Wiedza instytucjonalna (plik pułapek)

**Problem:** Agent trafia na nieoczywisty problem techniczny, rozwiązuje go po 15 minutach prób, a następna sesja zaczyna od zera i wpada w tę samą pułapkę.

**Rozwiązanie:** Dedykowany plik `pitfalls.md`, który zamienia błędy w wiedzę instytucjonalną.

```markdown
# Pułapki (nie powtarzać)

## Docker
- `docker compose` (v2), nie `docker-compose` (v1) na tym systemie
- Port 3000 używany przez dev server, nie binduj do niego

## API
- Rate limit na endpoint X to 10/min, nie 100/min jak sugeruje dokumentacja
- Token OAuth wygasa co 60 dni, monitoruj i odśwież

## Kodowanie plików
- CSV z Windows/Excel ma BOM (`\ufeff`) - użyj `encoding='utf-8-sig'`, nie `utf-8`
- JSON z trailing commas nie parsuje się standardowymi parserami

## Git
- Pre-commit hook uruchamia linting - napraw problemy, nie pomijaj przez --no-verify
- Branch main jest chroniony, zawsze używaj feature branchy
```

**Dlaczego to działa:** Claude Code nie sugeruje tworzenia takiego pliku. System pamięci CC jest generyczny - "zapisuj konwencje i wzorce". Plik pułapek to konkretna kategoria wiedzy o ekstremalnie wysokim stosunku wartości do rozmiaru. Jeden wpis (2 linie) oszczędza 15 minut debugowania w każdej przyszłej sesji.

**Jak utrzymywać:** Zapisuj pułapkę natychmiast po rozwiązaniu problemu. Nie odkładaj - zapomnisz kontekstu. Grupuj po technologii. Przeglądaj raz na kwartał i usuwaj nieaktualne.

## 3. Proaktywne zarządzanie rozmiarem pamięci

**Problem:** `MEMORY.md` rośnie z każdą sesją. Przy 200 liniach Claude Code obcina go - tracisz kontekst bez ostrzeżenia, często w połowie ważnej sekcji.

**Rozwiązanie:** Reguła 150 linii i algorytm aktualizacji.

### Reguła przepełnienia

```
Po każdym zapisie do MEMORY.md sprawdź liczbę linii.
Jeśli > 150 -> natychmiast wydziel największe sekcje do plików tematycznych.
Nigdy nie pozwól dojść do 200 (próg obcinania).
```

50-liniowy bufor daje margines bezpieczeństwa. Przy 150 liniach masz czas na reorganizację. Przy 200 jest już za późno.

### Algorytm aktualizacji

```
ZAPISUJ:
  - Konwencje potwierdzone w wielu interakcjach
  - Pułapki techniczne (-> pitfalls.md)
  - Nowe serwisy, skrypty, integracje
  - Zmiany konfiguracji wpływające na przyszłą pracę

NIE ZAPISUJ:
  - Bieżących zadań ani pracy w toku
  - Tymczasowego stanu ani jednorazowych poprawek
  - Niczego co duplikuje CLAUDE.md
  - Niesprawdzonych wniosków z czytania jednego pliku
```

**Dlaczego to działa:** CC mówi "max 200 linii" i tyle. Nie mówi co robić, żeby tam nie dojść. Algorytm aktualizacji rozwiązuje problem "co zapisać" (większość użytkowników zapisuje za dużo albo za mało), a reguła 150 rozwiązuje problem "kiedy wydzielić" (zanim będzie za późno).

### Wzorzec MEMORY.md jako indeks

```markdown
# Memory

## Autonomia agenta
Trzy poziomy: WOLNO / ZA ZGODĄ / NIGDY / ESKALACJA.
Pełna lista -> `memory/autonomy-rules.md`

## Serwer produkcyjny
Stack, porty, backup, SSL. Szczegóły -> `memory/server.md`

## Pułapki techniczne
Wszystkie -> `memory/pitfalls.md`

## Pliki tematyczne - czytaj gdy potrzebne
`autonomy-rules.md` | `pitfalls.md` | `server.md` | `tools.md`
```

Jednolinijkowe streszczenie + wskaźnik do pliku. Nigdy nie kopiuj treści - jedno źródło prawdy.

## Szybki start

### 1. Utwórz strukturę

```bash
mkdir -p ~/.claude/projects/$(basename "$PWD")/memory
```

### 2. Skopiuj szablony

```bash
git clone https://github.com/pawel-wyszomirski/claude-code-memory-framework.git /tmp/ccmf

# Instrukcje globalne (jeśli nie masz jeszcze CLAUDE.md):
cp /tmp/ccmf/templates/CLAUDE.md ~/.claude/CLAUDE.md

# Pliki pamięci dla projektu:
cp /tmp/ccmf/templates/MEMORY.md ~/.claude/projects/$(basename "$PWD")/memory/
cp /tmp/ccmf/templates/autonomy-rules.md ~/.claude/projects/$(basename "$PWD")/memory/
cp /tmp/ccmf/templates/pitfalls.md ~/.claude/projects/$(basename "$PWD")/memory/

rm -rf /tmp/ccmf
```

### 3. Dostosuj

- `CLAUDE.md` - język, formatowanie, preferencje behawioralne
- `autonomy-rules.md` - dodaj reguły specyficzne dla swojego środowiska
- `pitfalls.md` - uzupełniaj w trakcie pracy
- `MEMORY.md` - rośnie organicznie, pilnuj reguły 150

## Dobre praktyki

### Reguły absolutne, nie miękkie
"NIGDY nie commituj .env" zamiast "bądź ostrożny z .env". Agent stosuje się do jasnych reguł. Niejasne interpretuje po swojemu.

### Format dat
W plikach pamięci używaj `YYYY-MM-DD`. Nigdy "jutro", "w przyszłym tygodniu" - tracą sens pomiędzy sesjami.

### Wskaźniki, nie kopie
Nie duplikuj treści między plikami. `Szczegóły -> memory/plik.md`. Jedno źródło prawdy.

### Audyt bezpieczeństwa
Zapisuj w MEMORY.md kiedy ostatnio przejrzałeś sekrety. Ustaw sobie przypomnienie co miesiąc.

```markdown
## Bezpieczeństwo
- Ostatni audyt sekretów: 2025-06-01 (2 wycieki naprawione)
- Następny przegląd: 2025-07-01
```

### Comiesięczny przegląd pamięci
Pamięć się degraduje. Raz w miesiącu przejrzyj pliki, usuń nieaktualne wpisy, zaktualizuj zmienione. Plik pułapek - raz na kwartał.

## Co ten framework NIE robi

Dla jasności - te rzeczy są wbudowane w Claude Code i nie musisz ich konfigurować osobno:

- Ładowanie `CLAUDE.md` co sesję (wbudowane)
- Auto-ładowanie `MEMORY.md` (wbudowane)
- Katalog `memory/` z plikami tematycznymi (wbudowane)
- Semantyczna organizacja pamięci (sugerowana przez CC)
- Obcinanie po 200 liniach (wbudowane)

Ten framework buduje **na** tych mechanizmach, nie zastępuje ich.

## Dlaczego nie baza danych?

| Podejście | Zalety | Wady |
|-----------|--------|------|
| **SQLite + wektory** | Semantyczne wyszukiwanie | Złożona konfiguracja, nieprzejrzyste, szum |
| **Auto-zapis wszystkiego** | Zero wysiłku | Niski sygnał/szum, rozdęty kontekst |
| **Markdown + kuracja (to)** | Czytelne, wersjonowalne, audytowalne | Wymaga ręcznej kuracji |

Ręczna kuracja to cecha, nie wada. `cat memory/pitfalls.md` i widzisz dokładnie co agent wie. Wersjonujesz gitem. Przenosisz przez `scp`.

## Kontrybuowanie

Framework powstał w codziennym produkcyjnym użyciu. Jeśli odkryłeś wzorce, które dobrze współgrają z pamięcią Claude Code - PR-y i issues mile widziane.

## Licencja

MIT
