FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--certfile", "certificates/certificate.crt", "--keyfile", "certificates/private.key", "app:app"]