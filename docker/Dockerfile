FROM kalilinux/kali-rolling:latest

LABEL maintainer="Harsh Vardhan <harsh@cyberkill.ai>"
LABEL description="Cyberkill.ai Autonomous Multi-Agent Cybersecurity Platform"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install core system dependencies and Python
RUN apt-get update && apt-get install -y --no-install-recommends     python3     python3-pip     python3-venv     git     curl     nmap     masscan     sqlmap     nikto     whois     dnsutils     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN pip3 install -e .

EXPOSE 8888

ENTRYPOINT ["cyberkill"]
CMD ["server", "--host", "0.0.0.0", "--port", "8888"]
