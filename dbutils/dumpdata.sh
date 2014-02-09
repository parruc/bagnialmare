cd /var/www/ombrelloni.it/django
/var/www/ombrelloni.it/venv/bin/python manage.py dumpdata --indent=2 --exclude=south --exclude=sessions > ombrelloni/fixtures/dump.json
git commit ombrelloni/fixtures/dump.json -m "db dump"
git push
