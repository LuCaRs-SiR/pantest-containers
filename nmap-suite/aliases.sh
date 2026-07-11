# nmap_suite helper functions for this workspace
# Source this file in your shell to use the functions.

nmap_suite_shell() {
  docker run --rm -it --network host pantest-nmap-suite bash "$@"
}

nmap_suite_test() {
  docker run --rm --network host pantest-nmap-suite nmap --version
  echo '---'
  docker run --rm --network host pantest-nmap-suite nmap -sn 127.0.0.1
}

nmap_suite_scan() {
  docker run --rm --network host pantest-nmap-suite nmap "$@"
}

nmap_suite_nikto() {
  docker run --rm --network host pantest-nmap-suite nikto "$@"
}

nmap_suite_gobuster() {
  docker run --rm --network host pantest-nmap-suite gobuster "$@"
}

nmap_suite_sslscan() {
  docker run --rm --network host pantest-nmap-suite sslscan "$@"
}

nmap_suite_python() {
  docker run --rm --network host pantest-nmap-suite python3 "$@"
}

nmap_suite_pip() {
  docker run --rm --network host pantest-nmap-suite pip3 "$@"
}
