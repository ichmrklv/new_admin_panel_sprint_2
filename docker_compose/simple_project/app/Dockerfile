FROM python:3.9.6

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=example.settings

COPY requirements.txt requirements.txt

# hadolint ignore=DL3013 
# Все версии библиотек указаны в requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /var/www/static/ /var/www/media/ /opt/app/static/ /opt/app/media/

# Скрипт запуска и применения
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "example.wsgi:application", "--bind", "0.0.0.0:8000"]
