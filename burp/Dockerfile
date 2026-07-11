FROM eclipse-temurin:17-jre

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       libxext6 \
       libxrender1 \
       libxtst6 \
       libxi6 \
       libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

EXPOSE 8080

# Copy Burp JAR into this directory before building, for example:
# burpsuite_community.jar or burpsuite_pro.jar
# Then run with: docker run --rm -it -v "$PWD":/app burp java -jar /app/burpsuite_community.jar
CMD ["bash"]
