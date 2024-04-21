
FROM python:3.11-slim

ENV PYTHONUNBUFFERED = 1 \
    PIP_NO_CACHE_DIR = 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf var/lib/apt/lists/*

WORKDIR /app
RUN pip install -r requirements.txt

COPY . ./
EXPOSE 8080

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080" ]