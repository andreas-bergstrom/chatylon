# Chatylon

Simple server-rendered chat app.

![Chatylon user list](screenshot.png)

## Dependencies
- Django
- psycopg2
- django-crispy-forms
- django-debug-toolbar
- django-model-utils
- python-decouple
- django-redis-cache

## Instructions

1. Edit and rename default .env:
> docker-compose run web mv .default_env .env

2. Run Django migrations:
> docker-compose run web python manage.py migrate

3. Launch all containers:
> docker-compose up