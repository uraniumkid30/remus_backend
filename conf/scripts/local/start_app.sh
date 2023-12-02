#!/bin/bash
APP_NAME="general_services" # update to app_name

APP_TARGET_FOLDER="applications"
BASE_DIR=`pwd`
FULL_DIR="${BASE_DIR}/${APP_TARGET_FOLDER}/${APP_NAME}"
source conf/env_variables/.env
echo "${LIBRARY_MANAGER}"
echo "About creating ${APP_NAME} App in ${APP_TARGET_FOLDER} Folder"
echo "Current directory is ${BASE_DIR}"
echo "Full directory is ${FULL_DIR}"
if [ ${APP_NAME} ]
then
    if [ ${LIBRARY_MANAGER} == "poetry" ]
    then
        mkdir ${FULL_DIR}
        python manage.py startapp ${APP_NAME} ./${APP_TARGET_FOLDER}/${APP_NAME}
    elif [ ${LIBRARY_MANAGER} == "pipenv" ]
    then
        mkdir ${FULL_DIR}
        pipenv run python manage.py startapp ${APP_NAME} ./${APP_TARGET_FOLDER}/${APP_NAME}
    else
        mkdir ${FULL_DIR}
        python manage.py startapp ${APP_NAME} ./${APP_TARGET_FOLDER}/${APP_NAME}
    fi
fi