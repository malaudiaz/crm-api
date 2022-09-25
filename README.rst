Ejecutar:

poetry run python crm_api/main.py

Migraciones 

- Incial una migratios por primera vez

poetry run alembic init migrations

- General una migrations nueva a parti de cambios al modelo

poetry run alembic revision --autogenerate -m "comentario"

- Aplicar los cambios de la migratios

poetry run alembic upgrade head
