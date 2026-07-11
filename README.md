# Pentest Containers

## Uruchamianie

Ten projekt buduje narzędzia pentestowe w osobnych kontenerach.

Domyślnie używamy `docker compose`, ale w niektórych środowiskach klient Docker wymaga niższej wersji API niż serwer.

Jeżeli `docker compose` zwraca błąd:

> client version 1.43 is too old. Minimum supported API version is 1.44

to uruchamiaj polecenia z nadpisanym API:

```bash
DOCKER_API_VERSION=1.44 docker compose up -d nmap_suite
DOCKER_API_VERSION=1.44 docker compose logs --tail=50 nmap_suite
```

## Budowanie kontenera Recon Tools

Katalog: `recon`

Kontener zawiera:
- `subfinder`
- `amass`

Uruchom:

```bash
DOCKER_API_VERSION=1.44 docker compose build recon
DOCKER_API_VERSION=1.44 docker compose up -d recon
```

Test wewnątrz kontenera:

```bash
docker exec -it recon bash
subfinder -d example.com
amass enum -d example.com
```

Przykładowe komendy testowe:

```bash
subfinder -d example.com
amass enum -d example.com
```

## Budowanie kontenera HackAgent

Katalog: `hackagent`

Kontener zawiera:
- `hackagent` CLI
- lokalny kod źródłowy projektu do szybkiego rozwoju

Uruchom:

```bash
DOCKER_API_VERSION=1.44 docker compose build hackagent
DOCKER_API_VERSION=1.44 docker compose up -d hackagent
```

Test wewnątrz kontenera:

```bash
docker exec -it hackagent bash
python3 -c "import hackagent; print('hackagent ok')"
hackagent --help
```

## Budowanie kontenera AutoPentestX

Katalog: `autopentestx`

Kontener zawiera:
- AutoPentestX toolkit
- zależności z `requirements.txt`

Uruchom:

```bash
DOCKER_API_VERSION=1.44 docker compose build autopentestx
DOCKER_API_VERSION=1.44 docker compose up -d autopentestx
```

Test wewnątrz kontenera:

```bash
docker exec -it autopentestx bash
python3 /app/main.py --version
```

Jeśli chcesz uruchomić aplikację bezpośrednio:

```bash
docker exec -it autopentestx python3 /app/main.py -t example.com --no-safe-mode --skip-web
```

## Budowanie kontenera Inspector

Katalog: `inspector`

Kontener uruchamia narzędzie Inspector z katalogu `core`.

Uruchom:

```bash
DOCKER_API_VERSION=1.44 docker compose build inspector
DOCKER_API_VERSION=1.44 docker compose up -d inspector
```

Test wewnątrz kontenera:

```bash
docker exec -it inspector bash
python3 /app/core/inspector.py -h
```

Przykład uruchomienia:

```bash
docker exec -it inspector python3 /app/core/inspector.py +33666666666
```

Test automatyczny:

```bash
./inspector/test.sh
```

## Kolejność budowy narzędzi

1. `nmap_suite` (infrastruktura)
2. `recon` (powierzchnia ataku)
3. `hackagent`
4. `autopentestx`
5. `inspector`
6. `ollama`
7. `kali`
8. `burp` (opcjonalnie)

Potem: panel sterowania, integracja narzędzi, AI i workflow pentestowy.
