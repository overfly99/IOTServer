# ServerIOT
## Install Postgresql
- sudo apt update
- sudo apt install postgresql postgresql-contrib
- set password postgres = root
## Install mosquito 

## Install poetry
- curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
- source $HOME/.poetry/env
- poetry shell
- poetry install 
- cd demo
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py runserver
