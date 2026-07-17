# Panel Frontend

Frontend SvelteKit dla pentest cockpit.

## Struktura

- `src/routes/` — widoki panelu
- `src/components/` — elementy UI (na razie navbar)
- `src/lib/api.js` — wrapper do wywołań API

## Uruchomienie

```bash
cd panel/frontend
npm install
npm run dev -- --host
```

Dostępne pod `http://localhost:5173` (lub port wskazany przez Vite).
