# Bezpieczny Plan Odchudzenia Miejsca

## Stan obecny

- W `ollama-gpu/models` brak lokalnych plikow modeli (katalogi sa puste).
- W `~/.ollama` brak blobow modeli (jest glownie plik historii).
- Zduplikowany model embeddingowy znaleziony w dwoch rozszerzeniach VS Code:
  - `~/.vscode/extensions/autodidact613.continue613-1.0.9/models/all-MiniLM-L6-v2/onnx/model_quantized.onnx`
  - `~/.vscode/extensions/continue.continue-2.1.0-linux-x64/models/all-MiniLM-L6-v2/onnx/model_quantized.onnx`

## Zasady bezpieczenstwa

- Najpierw inwentaryzacja i backup, potem usuwanie.
- Nie usuwac katalogow aktywnego rozszerzenia bez potwierdzenia.
- Nie usuwac nic z repozytorium projektu bez commita i mozliwosci rollbacku.
- Po kazdym kroku sprawdzic dzialanie narzedzi (VS Code, rozszerzenia AI, kontenery).

## Plan krok po kroku

1. Zamknij aktywne sesje, ktore moga trzymac locki na plikach modeli.
2. Wykonaj snapshot rozmiaru katalogow:
   - `du -sh ~/.vscode/extensions/*/models ~/.cache/huggingface ~/.ollama 2>/dev/null`
3. Potwierdz aktywne rozszerzenie Continue w VS Code i wersje, ktorej uzywasz.
4. Jezeli jedno rozszerzenie jest nieuzywane, usun je przez VS Code (nie recznie):
   - najpierw uninstall starej wersji,
   - potem restart VS Code,
   - ponowny pomiar `du -sh`.
5. Oczysc cache Hugging Face tylko z logow i artefaktow tymczasowych:
   - usun stare pliki z `~/.cache/huggingface/xet/logs/` starsze niz 14 dni,
   - nie usuwaj katalogow `hub/models--*` bez audytu zaleznosci.
6. Zweryfikuj oszczednosc miejsca i sprawdz, czy embedding nadal dziala.
7. Opcjonalnie: ustaw okresowa rotacje logow (np. cotygodniowe czyszczenie logow xet).

## Czego nie robic

- Nie usuwac recznie losowych plikow `.onnx`, `.safetensors`, `.bin` bez sprawdzenia, kto ich uzywa.
- Nie usuwac calego `~/.cache/huggingface`, jesli narzedzia AI sa aktywnie uzywane.
- Nie modyfikowac `ollama-gpu/` kluczami SSH i uprawnieniami bez celu operacyjnego.

## Szybki rollback

- Jesli po cleanupie cos przestaje dzialac:
  - zainstaluj ponownie wymagane rozszerzenie,
  - uruchom ponownie VS Code,
  - pozwol rozszerzeniu odtworzyc brakujace modele lokalnie.