#!/bin/bash
source conf/env_variables/.env
echo "${LIBRARY_MANAGER}"
if [ ${LIBRARY_MANAGER} == "poetry" ]
then
    poetry shell
    poetry install
    poetry lock --no-update
    source $(poetry env info --path)/bin/activate
    python manage.py check
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8000
elif [ ${LIBRARY_MANAGER} == "pipenv" ]
then
    echo "${blue}>>> Syncing environment with with ${LIBRARY_MANAGER}."
    pipenv shell
    pipenv sync
    echo "${green}>>> About running development server with ${LIBRARY_MANAGER}."
    pipenv run python manage.py check
    pipenv run python manage.py migrate
    pipenv run python manage.py runserver 0.0.0.0:8000
else
    echo "${blue}>>> Syncing environment with with ${LIBRARY_MANAGER}."
    echo "${green}>>> About running development server with ${LIBRARY_MANAGER}."
    python manage.py check
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8000
fi
