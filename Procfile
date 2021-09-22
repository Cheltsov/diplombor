web: gunicorn diplombor.wsgi --log-file -
release: python manage.py migrate
python manage.py collectstatic --no-input
