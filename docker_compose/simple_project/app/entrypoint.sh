#!/bin/sh

# цикл ожидания запуска БД
echo "Waiting for database to be ready at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for $DB_HOST:$DB_PORT..."
  sleep 0.1
done

echo "Database is up!"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@" # передача gunicorn
