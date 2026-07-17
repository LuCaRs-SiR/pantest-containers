# Kali Tools Container

Ten katalog zawiera konfigurację kontenera Kali, który jest przeznaczony do uruchamiania standardowych narzędzi pentestowych w izolowanym środowisku.

## Cel

Kontener `kali-tools` ma zapewnić szybki dostęp do narzędzi Kali bez konieczności instalacji całego systemu Kali na hoście. Dzięki mapowaniu katalogu `./kali-tools` do `/tools` możesz łatwo przechowywać własne skrypty i wyniki.

## Zainstalowane narzędzia

- nmap
- sqlmap
- hydra
- john
- nikto
- gobuster
- curl
- wget
- git
- net-tools
- dnsutils
- iputils-ping
- python3
- python3-pip
- sudo

## Budowa i uruchomienie

```bash
docker compose build kali
```

```bash
docker compose up -d kali
```

## Wejście do kontenera

```bash
docker exec -it kali-tools bash
```

## Przykładowe użycie

```bash
nmap -sC -sV 192.168.1.1
```

```bash
sqlmap -u "http://example.com/vuln.php?id=1" --batch
```

```bash
gobuster dir -u http://example.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

## Rozszerzenia

Do `./kali-tools` możesz dodać własne skrypty i dane rozwiązując je w kontenerze przez `/tools`.
