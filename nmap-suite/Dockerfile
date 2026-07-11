FROM kalilinux/kali-rolling

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       nmap \
       nikto \
       gobuster \
       sslscan \
       python3 \
       python3-pip \
       git \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tools
COPY . /tools

CMD ["bash"]
