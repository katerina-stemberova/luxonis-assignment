FROM python:3.11

RUN pip install Flask \
    psycopg2-binary

COPY . /app

WORKDIR /app

CMD ["python", "app.py"]
