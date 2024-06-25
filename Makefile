start:
	docker compose build web
	docker compose run web python manage.py migrate
	docker compose run web python manage.py loaddata seed/*

start_db:
	docker compose up -d db

stop_db:
	docker compose down db

run:
	docker compose up

stop:
	docker compose down