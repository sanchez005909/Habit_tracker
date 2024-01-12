1) pip install -r requirements.txt
2) python manage.py migrate
3) python manage.py bot
4) celery -A config beat -l INFO -S django
5) celery -A config worker -l INFO 

