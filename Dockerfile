FROM nikolaik/python-nodejs:python3.13-nodejs23-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME [ "/app/data" ]

CMD ["python", "main.py"]
