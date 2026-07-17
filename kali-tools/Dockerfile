FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      curl \
      wget \
      nmap \
      net-tools \
      dnsutils \
      iputils-ping \
      sudo \
      python3 \
      python3-pip \
      ca-certificates \
      sqlmap \
      hydra \
      john \
      nikto \
      gobuster \
      tmux \
      vim \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /tools
COPY . /tools

CMD ["/bin/bash"]
