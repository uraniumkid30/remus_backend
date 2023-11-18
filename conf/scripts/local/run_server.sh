#!/bin/bash

# source ./venv/bin/activate
# sleep 2


# # migrate
# python manage.py makemigrations
# python manage.py migrate

# create superuser
# echo "${green}>>> Creating a 'admin' user ...${reset}"
# echo "${green}>>> The password must contain at least 8 characters.${reset}"
# echo "${green}>>> Password suggestions: djangoadmin${reset}"
# python manage.py createsuperuser --username='admin' --email=''

# run
source conf/env_variables/.env
if [ ${LIBRARY_MANAGER} == "poetry" ]
then
    poetry shell
    poetry install
    poetry lock --no-update
    source $(poetry env info --path)/bin/activate
    python manage.py check
    python manage.py runserver
elif [ ${LIBRARY_MANAGER} == "pipenv" ]
then
    echo "${blue}>>> Syncing environment with with ${LIBRARY_MANAGER}."
    pipenv shell
    echo "${green}>>> About running development server with ${LIBRARY_MANAGER}."
    pipenv run python manage.py check
    pipenv run python manage.py runserver
else
    echo "${blue}>>> Syncing environment with with ${LIBRARY_MANAGER}."
    echo "${green}>>> About running development server with ${LIBRARY_MANAGER}."
    python manage.py check
    python manage.py runserver
fi
