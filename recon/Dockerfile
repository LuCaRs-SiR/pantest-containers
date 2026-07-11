FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       git \
       curl \
       wget \
       unzip \
       tar \
       python3 \
       python3-pip \
       ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Subfinder
RUN curl -sL https://github.com/projectdiscovery/subfinder/releases/download/v2.14.0/subfinder_2.14.0_linux_amd64.zip -o /tmp/subfinder.zip \
    && unzip /tmp/subfinder.zip -d /tmp/subfinder \
    && mv /tmp/subfinder/subfinder /usr/local/bin/subfinder \
    && chmod +x /usr/local/bin/subfinder \
    && rm -rf /tmp/subfinder /tmp/subfinder.zip

# Install Amass
RUN curl -sL https://github.com/owasp-amass/amass/releases/download/v5.1.1/amass_linux_amd64.tar.gz -o /tmp/amass.tar.gz \
    && mkdir -p /opt/amass \
    && tar -xzf /tmp/amass.tar.gz -C /opt/amass --strip-components=1 \
    && ln -s /opt/amass/amass /usr/local/bin/amass \
    && chmod +x /usr/local/bin/amass \
    && rm -rf /tmp/amass.tar.gz

WORKDIR /tools
CMD ["bash"]
