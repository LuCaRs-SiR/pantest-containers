FROM kalilinux/kali-rolling

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      curl \
      wget \
      nmap \
      net-tools \
      dnsutils \
      iputils-ping \
      sudo && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tools

CMD ["/bin/bash"]
