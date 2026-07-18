# PR Description: Sync Repo State With Current Workspace

## Cel

- Synchronizacja repozytorium z aktualnym stanem lokalnego srodowiska projektu.
- Uporzadkowanie dokumentacji i zasad wersjonowania artefaktow runtime.

## Zakres zmian

- Aktualizacja `README.md` o aktualny stan katalogu glownego i kluczowe elementy projektu.
- Aktualizacja `.gitignore` o wykluczenie raportow runtime z `logs/assistant-reports`.
- Aktualizacja logiki orkiestracji w `panel/backend/app/services/orchestrator.py`:
  - detekcja dostepnych narzedzi w kontenerach,
  - budowanie planu zaleznie od faktycznych mozliwosci srodowiska,
  - rozszerzenie krokow web/api/infra/ad,
  - bezpieczniejsze skladanie komend.

## Dlaczego

- Repozytorium ma lepiej odzwierciedlac faktyczny stan projektu.
- Ograniczenie przypadkowego commitowania plikow generowanych dynamicznie.
- Stabilniejsze planowanie zadan asystenta w zaleznosci od dostepnych narzedzi.

## Wplyw

- Brak zmian breaking changes.
- Zmiany dotycza dokumentacji, regul ignorowania i logiki planera backendu.

## Walidacja

- Sprawdzono skladnie pliku `orchestrator.py` przez parsowanie AST.
- Commit zostal wypchniety na galaz `sync-with-devin`.

## Dane commita

- Hash: `0704256`
- Pliki:
  - `README.md`
  - `.gitignore`
  - `panel/backend/app/services/orchestrator.py`