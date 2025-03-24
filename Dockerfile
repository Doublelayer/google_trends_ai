FROM nikolaik/python-nodejs:python3.13-nodejs23-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    lsof \
    apt-transport-https \
    ca-certificates \
    x11-utils xdg-utils xvfb \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/* \

# Add the Google Chrome repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# USER gitpod

# Add the Chrome as a path variable
ENV CHROME_BIN=/usr/bin/google-chrome

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME [ "/app/data" ]

CMD ["python", "main.py"]
