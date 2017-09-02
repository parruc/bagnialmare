#!/bin/bash
mkdir -p /project/bagnialmare/bagnialmare/whoosh_index/en /project/bagnialmare/bagnialmare/whoosh_index/it /var/log/django/email
cd /project/bagnialmare
/project/bin/python manage.py collectstatic --noinput
chown www-data:www-data /var/www/static/ -R
chown www-data:www-data /var/www/media/ -R
/project/bin/python manage.py makemigrations
/project/bin/python manage.py migrate
/project/bin/python manage.py manage_index -o create
/project/bin/python manage.py compilemessages
/project/bin/python manage.py manage_index -o rebuild
chown www-data:www-data /project/bagnialmare/bagnialmare/whoosh_index /var/log/django -R
