FROM python:3.10

# Create a non-root user and group
RUN groupadd -r myusergroup && useradd -r -g myusergroup myuser

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

USER myuser

CMD ["python", "app.py"]