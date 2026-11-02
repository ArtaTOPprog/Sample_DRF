FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

ARG REQUIREMENTS=requirements/base.txt
COPY requirements ./requirements
RUN pip install -r ${REQUIREMENTS}

RUN addgroup --system app && adduser --system --ingroup app app

COPY --chown=app:app . .

RUN DJANGO_SECRET_KEY=collectstatic DJANGO_SETTINGS_MODULE=config.settings.production \
    python manage.py collectstatic --noinput \
    && mkdir -p media && chown -R app:app staticfiles media

USER app

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --access-logfile -"]
