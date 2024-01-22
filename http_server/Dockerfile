FROM python:3.11

# install dependencies for Flask and connection to Postgres
RUN pip install Flask \
    psycopg2-binary

# copy the project
COPY . /app

# cd to the project dir
WORKDIR /app

# entrypoint - run the server when the container starts
CMD ["python", "app.py"]
