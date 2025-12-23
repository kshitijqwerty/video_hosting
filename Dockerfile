FROM python:3.12-slim

# System deps

RUN apt update && apt install -y \
    ffmpeg \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# project files

COPY . .

RUN mkdir -p /app/media

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=ytclone.settings

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]