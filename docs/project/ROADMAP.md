# Roadmapa projektu Pentest Containers

Ten projekt ma rosnąć w kierunku profesjonalnego, modularnego środowiska pentestowego z panelem sterowania, integracją AI i raportowaniem.

## Krótkoterminowe cele

- Dokumentacja repozytorium: pełny `README.md`, `ROADMAP.md`, `LICENSE` i `.gitignore`
- Stabilny `docker-compose.yml` dla wszystkich modułów
- Własne `Dockerfile` dla każdej usługi:
  - `nmap-suite`
  - `recon`
  - `hackagent`
  - `autopentestx`
  - `inspector`
  - `ollama-gpu` (stan i konfiguracja lokalna)
  - `kali-tools`
  - `burp` (opcjonalnie)
- Umożliwienie szybkiego uruchamiania i testowania narzędzi w kontenerach

## Średnioterminowe cele

- Integracja lokalnej maszyny Ollama GPU z kontenerami
- Budowa prostego panelu sterowania do zarządzania usługami przez Docker SDK
- Przygotowanie backendu API do uruchamiania skanów i pobierania wyników
- Rejestracja wyników skanów i raportów w formacie JSON/HTML
- Dodanie historii i logów narzędzi w panelu
- Rozszerzenie modułów o obsługę:
  - testów API
  - testów aplikacji webowych
  - testów infrastruktury i sieci

## Długoterminowe cele

- Frontend panelu sterowania w React lub Svelte
- Integracja z AI do automatyzacji i analizy wyników
- Workflow pentestowy: rozpoznanie → skanowanie → eksploitacja → raportowanie
- Multi-user / rola operatora w panelu sterowania
- Zbieranie i wizualizacja metryk oraz historii zadań
- Możliwość dodawania własnych modułów narzędziowych i wtyczek

## Architektura przyszłego panelu

1. Backend:
   - FastAPI / Python
   - Docker SDK do zarządzania kontenerami i zadaniami
   - baza danych do wyników, historii zadań i użytkowników
2. Frontend:
   - Svelte lub React
   - panel z widokiem statusu kontenerów, logami i wynikami
3. Integracja z AI:
   - lokalny Ollama GPU
   - automatyzacja raportów
   - sugestie następnych kroków pentestowych
   - rekomendowane modele: Qwen 2.5 14B Instruct, DeepSeek R1, LLaMA 3.1

## Panel sterowania — konkretne funkcje

- Globalny dashboard stanu usług:
  - status kontenerów (`running`, `stopped`, `restarting`)
  - wykorzystanie zasobów, uruchomione narzędzia i czas działania
- Operacje kontenera:
  - start / stop / restart / rebuild modułów
  - podgląd bieżącej konfiguracji i wersji obrazu
- Menedżer zadań pentestowych:
  - tworzenie i kolejka zadań skanowania
  - parametryzowane profile skanów (network, recon, web, infra)
  - harmonogramy i zadania jednorazowe
- Podgląd wyników i logów:
  - live stream logów z kontenerów
  - zapis logów i wyników do plików JSON/HTML
  - historyczny dostęp do poprzednich zadań
- Szablony i workflow:
  - gotowe szablony dla `nmap`, `amass`, `subfinder`, `nikto`, `gobuster`
  - definiowanie własnych kroków pentestu
  - automatyczne przejście od rozpoznania do skanowania i raportowania
- Raportowanie:
  - eksport wyników do HTML/PDF/JSON
  - generowanie szybkich podsumowań ryzyk
  - flagowanie podmiotów do dalszej analizy
- Integracja AI:
  - rekomendacje kolejnych testów na podstawie wyników
  - klasyfikacja i priorytetyzacja znalezionych usług
  - generowanie uogólnień z danych skanowania
- Bezpieczeństwo i kontrola dostępu:
  - prosta autoryzacja użytkowników
  - role operator / administrator
  - zapis audytu działań
- Rozszerzalność:
  - pluginy / moduły narzędziowe
  - możliwość dodawania nowych kontenerów i narzędzi przez UI
  - integracja z systemem plików hosta i katalogiem raportów

## Najważniejsze kamienie milowe

1. Pełny, działający `docker compose` dla wszystkich modułów
2. Dokumentacja dla użytkownika i developera
3. Lokalna instalacja Ollama GPU i test modelu
4. Pierwsza wersja panelu sterowania z backendem API
5. Raportowanie wyników skanów i historia zadań
6. Automatyzacja workflow: recon -> scan -> analyze -> report
