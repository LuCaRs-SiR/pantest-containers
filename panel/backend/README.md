# Panel Backend

Backend FastAPI dla pentest cockpit, który integruje się z kontenerami narzędziowymi i AI Gateway.

## Struktura

- `main.py` — główny serwer FastAPI
- `services/ollama.py` — integracja z AI Gateway
- `services/tool_runner.py` — uruchamianie narzędzi w kontenerach
- `requirements.txt` — zależności

## Funkcje

- `GET /status` — sprawdza stan backendu
- `POST /run/nmap` — uruchamia `nmap` w kontenerze `nmap-suite`
- `POST /run/recon` — uruchamia `subfinder` i `amass` w kontenerze `recon`
- `POST /run/inspector` — uruchamia narzędzie `inspector`
- `POST /run/hackagent` — uruchamia zadanie w kontenerze `hackagent`
- `POST /run/autopentestx` — uruchamia zadanie w kontenerze `autopentestx`
- `GET /history` — pobiera historię wykonanych zadań
- `GET /logs/{tool_name}` — pobiera logi narzędzia
- `POST /report` — generuje raport przy użyciu lokalnego AI Gateway

## Zależności

- FastAPI
- Uvicorn
- Docker SDK
- Requests

## Uruchomienie

1. Zbuduj kontener:

```bash
cd panel/backend
docker build -t pantest-panel-backend .
```

2. Uruchom kontener przez `docker compose`.

## Konfiguracja

`AI_GATEWAY_URL` można nadpisać przez zmienną środowiskową w `docker-compose.yml`.
