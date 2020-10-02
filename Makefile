run:
	 python dojopuzzles/manage.py runserver

migrate:
	python dojopuzzles/manage.py migrate

update-static-files:
	sudo rm -rf  staticfiles/* && python manage.py collectstatic
