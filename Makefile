build:
	docker compose build web

start:
	docker compose up web

stop:
	docker compose down web

seed_db:
	docker compose run web python manage.py loaddata seed/*

start_db:
	docker compose up -d db

stop_db:
	docker compose down db
