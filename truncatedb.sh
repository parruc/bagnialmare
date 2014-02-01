../venv/bin/python manage.py sqlflush | sed 's/TRUNCATE \(.*\);/TRUNCATE \1 CASCADE;/g' | ../venv/bin/python manage.py dbshell
