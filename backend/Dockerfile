FROM python:3.10

# Create a non-root user and group
RUN groupadd -r myusergroup && useradd -r -g myusergroup myuser

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

USER myuser

# add -w option to gunicorn to specify number of workers, default to 1
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--certfile", "certificates/certificate.crt", "--keyfile", "certificates/private.key", "--worker-class", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "app:app"]