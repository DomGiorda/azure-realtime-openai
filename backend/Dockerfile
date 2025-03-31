FROM python:3.12-slim

WORKDIR /app
COPY . /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m pip install -r requirements.txt

RUN python -m pip install gunicorn

CMD ["python3", "-m", "gunicorn", "app:create_app", "-b", "0.0.0.0:8765", "--worker-class", "aiohttp.GunicornWebWorker"]
EXPOSE 8765