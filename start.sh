find . -name "*.pyc" -type f -delete
SEVERUS_DEBUG=1 python manage.py runserver 0.0.0.0:8000 --noreload
