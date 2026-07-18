# Pentest Containers

<p align="center">
	<img src="assets/hero/repo-hero.jpg" alt="Pentest Containers Hero" width="100%" />
</p>

Modularny, konteneryzowany zestaw narzędzi pentestowych do rozpoznania, automatyzacji i inspekcji.

Ten projekt jest zbudowany jako zbiór niezależnych kontenerów, które można uruchamiać osobno lub razem przez `docker compose`. Każdy moduł ma własny katalog, Dockerfile oraz lokalny kod źródłowy, aby zapewnić skalowalność i szybki rozwój.

## Wizualizacja architektury

Sekcja prezentuje widok high-level oraz przepływ operacyjny między modułami. Uklad jest celowo uproszczony, aby szybko pokazywac strukture projektu bez nadmiaru detali.

### Executive View

- Platforma laczy narzedzia pentestowe, warstwe AI i panel operacyjny w jednym, modularnym stacku kontenerowym.
- Orkiestracja przez `docker compose` upraszcza uruchamianie, skalowanie i utrzymanie srodowiska.
- Architektura wspiera scenariusze od rozpoznania po raportowanie i automatyzacje dzialan.

### Architecture Overview

<img src="assets/architecture/architecture-overview.jpg" alt="Architektura projektu" width="100%" />

Opis:
Widok topologii systemu pokazuje relacje miedzy kontenerami narzedziowymi, warstwa AI oraz panelem zarzadzania. Diagram sluzy jako mapa komponentow i punkt wejscia dla onboarding'u technicznego.

### Operational Flow

<img src="assets/architecture/architecture-flow.jpg" alt="Przeplyw miedzy modulami" width="100%" />

Opis:
Widok przeplywu operacyjnego prezentuje kolejnosc dzialan i wymiane danych miedzy modulami. Ulatwia zrozumienie przebiegu procesu od uruchomienia narzedzi, przez analize, do generowania wynikow i raportow.

### Architecture At A Glance

- **Model wdrożenia:** modularny stack kontenerowy uruchamiany przez `docker compose`
- **Warstwa AI:** `ollama-gpu` + `ai-gateway` + `panel/backend`
- **Warstwa operacyjna:** `nmap-suite`, `recon`, `kali-tools`, `inspector`, `autopentestx`, `hackagent`
- **Warstwa prezentacji:** `panel/frontend` (SvelteKit)
- **Telemetria i artefakty:** centralny katalog `logs/`

## Co znajduje się w repozytorium

- `docker-compose.yml` — główny orchestrator wszystkich usług
- `nmap-suite/` — kontener z narzędziami do skanowania sieci
- `recon/` — kontener z narzędziami do rozpoznania powierzchni ataku
- `hackagent/` — kontener HackAgent AI/automation
- `autopentestx/` — kontener AutoPentestX
- `inspector/` — kontener Inspector
- `ollama-gpu/` — lokalny katalog stanu Ollama i konfiguracja GPU
- `ai-gateway/` — FastAPI wrapper dla lokalnego serwera Ollama i modeli AI
- `panel/backend/` — backend FastAPI dla panelu sterowania, logów i integracji AI
- `panel/frontend/` — SvelteKit frontend do obsługi panelu sterowania
- `kali-tools/` — kontener z narzędziami Kali
- `burp/` — opcjonalny kontener Burp Suite
- `logs/` — centralny katalog logów i raportów asystenta
- `LOGS.md` — opis konwencji logowania i ścieżek logów
- `LICENSE` — licencja open-source MIT
- `ROADMAP.md` — plan dalszego rozwoju projektu

## Cel projektu

To repozytorium ma być profesjonalnym fundamentem środowiska pentestowego:

- modularne kontenery narzędziowe
- centralne zarządzanie przez `docker compose`
- możliwości integracji z AI i lokalnym modelem Ollama
- ścieżka rozwoju w kierunku panelu sterowania, API i raportowania

## Wymagania

- Docker Engine 20.10+ (Linux zalecany)
- Docker Compose v2 / `docker compose`
- NVIDIA Container Toolkit, jeżeli chcesz uruchomić `ollama-gpu`
- Opcjonalnie: `DOCKER_API_VERSION=1.44`, gdy klient Docker ma starsze API niż serwer

## Szybki start

1. Zbuduj wszystkie moduły:

```bash
docker compose build
```

2. Uruchom wybrane moduły, np.:

```bash
docker compose up -d nmap_suite recon hackagent autopentestx inspector ollama panel kali burp
```

3. Wejdź do kontenera:

```bash
docker exec -it nmap-suite bash
```

4. Uruchom narzędzie w środku, np.:

```bash
nmap -sC -sV 192.168.1.1
```

Jeżeli napotkasz błąd API klienta:

```bash
DOCKER_API_VERSION=1.44 docker compose up -d nmap_suite
```

## Usługi i moduły

### `nmap_suite`

Narzędzia do skanowania sieci i hostów. Domyślnie uruchamiany w katalogu `/tools`.

### `recon`

Narzędzia do rozpoznania domeny i infrastruktury. W pakiecie znajdują się m.in. `subfinder` oraz `amass`.

### `hackagent`

Lokalny kontener HackAgent z kodem źródłowym do szybkiego developmentu i testowania CLI.

### `autopentestx`

Kontener AutoPentestX z zależnościami zdefiniowanymi w `autopentestx/requirements.txt`.

### `inspector`

Kontener do inspekcji i analizy, uruchamiający skrypty Python z katalogu `inspector/core`.

### `ollama`

Lokalny serwer Ollama z obsługą GPU. Przechowuje stan w katalogu `ollama-gpu`.

### `panel`

Backend AI dla panelu sterowania, który łączy się z lokalnym Ollama i oferuje endpointy do generowania raportów, PoC, analizy logów i kodu.

### `kali`

Kontener z narzędziami Kali do zadań zaawansowanych.

### `burp`

Opcjonalny kontener Burp Suite, przeznaczony do integracji z resztą środowiska.

## Przykładowe komendy

Uruchomienie kontenera `recon`:

```bash
docker compose build recon
```

```bash
docker compose up -d recon
```

Test w kontenerze `recon`:

```bash
docker exec -it recon bash
subfinder -d example.com
amass enum -d example.com
```

Sprawdzenie `hackagent`:

```bash
docker exec -it hackagent bash
python3 -c "import hackagent; print('hackagent ok')"
hackagent --help
```

Sprawdzenie `autopentestx`:

```bash
docker exec -it autopentestx bash
python3 /app/main.py --version
```

Sprawdzenie `inspector`:

```bash
docker exec -it inspector bash
python3 /app/core/inspector.py -h
```

## Rozwój projektu

Zobacz `ROADMAP.md` po szczegóły dotyczące kolejnych etapów rozwoju projektu.

## Aktualny stan katalogu głównego (2026-07-18)

Aktualna struktura katalogu głównego obejmuje:

- `ai-gateway/`
- `autopentestx/`
- `burp/`
- `hackagent/`
- `inspector/`
- `kali-tools/`
- `logs/`
- `nmap-suite/`
- `ollama-gpu/` (lokalny stan runtime, domyślnie poza kontrolą wersji)
- `panel/` (`backend/` + `frontend/`)
- `recon/`

Pliki główne:

- `docker-compose.yml`
- `README.md`
- `ROADMAP.md`
- `LOGS.md`
- `LICENSE`

## Licencja

Projekt jest dostępny na licencji MIT. Zobacz `LICENSE`.
