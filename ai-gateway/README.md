# Panel Backend AI

Ten katalog zawiera prosty backend FastAPI, który integruje się z lokalnym serwerem Ollama i udostępnia API dla panelu sterowania pentestowego.

## Funkcje

- endpointy dla ogólnego wnioskowania modeli
- generowanie raportów pentestowych
- generowanie PoC
- analiza logów
- analiza fragmentów kodu i konfiguracji
- wsparcie dla rekomendowanych modeli: Qwen 2.5, DeepSeek R1, LLaMA 3.1

## Budowa i uruchomienie

```bash
docker compose build panel
```

```bash
docker compose up -d panel
```

## Endpointy

- `GET /health` — sprawdza dostępność usługi i Ollama
- `GET /models` — zwraca mapę skonfigurowanych modeli
- `POST /infer` — ogólny punkt wnioskowania
- `POST /generate_report` — generuje raport pentestowy
- `POST /generate_poc` — generuje PoC
- `POST /analyze_logs` — analizuje logi
- `POST /analyze_code` — analizuje kod

## Konfiguracja

Domyślny adres Ollama jest ustawiony w zmiennej środowiskowej `OLLAMA_URL`.

Domyślny model AI Gateway jest ustawiony przez `OLLAMA_MODEL` na:

`qwen2.5-coder:7b`

## Auto-start modelu Qwen przy starcie panelu

W `docker-compose.yml` skonfigurowane są:

- `ollama` z `gpus: all` (uruchomienie z akceleracją GPU)
- `ollama-init` (jednorazowy bootstrap), który:
	- czeka na gotowość Ollama,
	- wykonuje `pull` modelu `qwen2.5-coder:7b`,
	- wykonuje warmup modelu z `keep_alive=24h`, aby model utrzymywał się w pamięci GPU.

Dzięki temu po uruchomieniu panelu model Qwen jest automatycznie przygotowany
do obsługi zapytań bez ręcznego pull/ping.

W `docker-compose.yml` usługa `panel` jest skonfigurowana z wartością:

```bash
OLLAMA_URL=http://ollama-gpu:11434
```

## Rekomendowane modele Ollama

Ten projekt jest zoptymalizowany pod lokalne modele Ollama dla pentestu:

- `qwen_2.5_14b_instruct` — główny model do analizy kodu, API, PoC i raportów
- `deepseek_r1` — model reasoning do złożonych przypadków, analizy logiki i autoryzacji
- `llama3.1_8b` — model językowy do pisania opisów, raportów i komunikacji klientowej

Jeśli nazwy modeli różnią się w Twoim środowisku, zaktualizuj `panel-backend/config.py`.

Jeśli model nie jest dostępny, zaktualizuj `panel-backend/config.py` z prawidłowym identyfikatorem modelu.
