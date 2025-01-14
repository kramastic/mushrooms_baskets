Здравствуйте!

Для хранения данных используется  Postgresql.
Для подкючения к бд необходимо создать файл .env следующего типа:
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=

и выполнить миграции
alembic revision --autogenerate -m 'Initial migration'
alembic upgrade head
