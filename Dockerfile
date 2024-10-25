FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt update -y && apt-get install -y libpq-dev && pip install --no-cache-dir -r requirements.txt

COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the Alembic migrations before starting the application
CMD ["bash", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
