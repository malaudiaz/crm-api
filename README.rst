Ejecutar:

poetry run python crm_api/main.py

Migraciones 

- Incial una migratios por primera vez

poetry run alembic init migrations

- General una migrations nueva a parti de cambios al modelo

poetry run alembic revision --autogenerate -m "comentario"

- Aplicar los cambios de la migratios

poetry run alembic upgrade head


GitHub

---------------------------------------------
url: https://github.com/malaudiaz/crm-api
username: malaudiaz
password: Pi=3.1416xx
token: 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

---------------------------------------------

git status                  --->    Para ver el estado de nuestro archivos

git add .                   --->    Para adicionar todos los archivos al staging area
git add README.rst          --->    Para adicionar el archivo README.rst al staging area

git commit -m "comentario"  --->    Para crear un punto de control en nuestro codigo

git log                     --->    Para ver todos los commits que hemos creado

git checkout -- README.rst  --->    Para revertir los cambios de los archivos

git diff                    --->    Para ver las diferencias hechas en los archivos

git branch                  --->    Muestras las versiones que existen ej. master

git branch login            --->    Comienza una nueva versión del proyecto si alterar la anterior (rama)

git checkout login          --->    Cambia a la rama Login


- Para descargar el proyecto

git clone https://github.com/malaudiaz/crm-api.git

cd crm-api

poetry init

poetry shell

poetry add fastapi uvicorn alembic psycopg2-binary itsdangerous passlib fastapi-sqlalchemy python-dotenv PyJWT

poetry run python crm_api/main.py 

-------
