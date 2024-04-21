FROM python:3.11-slim
WORKDIR /app

ENV PYTHONUNBUFFERED = 1 \
    PIP_NO_CACHE_DIR = 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 7000

COPY . ./
CMD [ "python", "consumer.py" ]


