FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../app/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN if [ "$FLASK_ENV" = "production" ]; then pip install gunicorn; fi

COPY ../app .

CMD if [ "$FLASK_ENV" = "production" ]; then pip install gunicorn && gunicorn -b 0.0.0.0:5000 app:app -w 3; fi && \
flask run --host=0.0.0.0 --reload