release: python manage.py migrate; python manage.py create_access_token;
web: gunicorn concert_play.wsgi:application --log-file -