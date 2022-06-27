FROM python:3.10

COPY entrypoint.sh /entrypoint.sh
COPY . /app

WORKDIR /app

RUN pip install -U pip \
    && pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
