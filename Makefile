dependencies:
	sudo apt install python3 python3-dev python3-virtualenv postgresql nodejs npm

virtualenv:
	virtualenv --python=python3 .
	./bin/pip install -r requirements.txt

node:
	cd layout; npm install; cd ..

init: dependencies virtualenv node

makemigrations:
	docker exec -i -t -w /project/bagnialmare/ bagnialmare_django_1 ../bin/python manage.py makemigrations --noinput

migrate:
	docker exec -i -t -w /project/bagnialmare/ bagnialmare_django_1 ../bin/python manage.py migrate --noinput

makemessages:
	docker exec -i -t -w /project/bagnialmare/authauth/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/bagnialmare/bagnialmare/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/bagnialmare/bagni/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/bagnialmare/booking/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/bagnialmare/contacts/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/bagnialmare/multilingual/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/bagnialmare/newsletters/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a
	docker exec -i -t -w /project/bagnialmare/userfeedback/ bagnialmare_django_1 ../../bin/python ../manage.py makemessages -a

compilemessages:
	docker exec -i -t -w /project/bagnialmare/authauth/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/bagnialmare/bagnialmare/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/bagnialmare/bagni/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/bagnialmare/booking/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/bagnialmare/contacts/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/bagnialmare/multilingual/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/bagnialmare/newsletters/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker exec -i -t -w /project/bagnialmare/userfeedback/ bagnialmare_django_1 ../../bin/python ../manage.py compilemessages
	docker restart bagnialmare_django_1

theme:
	docker exec -i -t -w /project/bagnialmare/ bagnialmare_django_1 ../bin/python manage.py collectstatic --noinput
	docker restart bagnialmare_django_1
