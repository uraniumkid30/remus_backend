# Remus Backend API DJango Version
# Requirements
pipenv
pyenv (python 3.9)

# Project Setup
## Once pipenv is installed you can execute the following command
`python local 3.9.10` this will set your local project to python 3.9
`pipenv shell` this will create a virtual environment.
`pipenv sync`  This will install all the required package and
 also create a virtual environment if needed.

## ENV FILE Updates
- `pipenv run python services/utilities.py` this will create a secret key to the terminal,
copy it and use it in your .env file for the SECRET_KEY constant

- update the database settings if using postgres or mysql

## manage.py updates
- `conf/scripts/local/start.sh` to start server for the first time
- `conf/scripts/local/run_server.sh` to start server subsequent times
- `conf/scripts/local/kill_server.sh` to kill server

# HOWTO Development
 to use the development settings.  
Example:
```
pipenv run python manage.py command 
```

# How to run a script file
``` 
chmod u+x file.sh 
./file.sh
```

# HOW TO Contribute
Before First Commit or on update of the `.pre-commit-config.yaml` file, run :
either 
```
pre-commit install 
```
or 
```
pipenv run pre-commit install
```

This will install pre-commits lattest settings at .git/hooks/pre-commit.

# Directory Notes:
- New apps should go into the `Applications` Directory.
- Urls for each app should go into `Applications.urls.py` file.
- Django setting Constants should go into files that reside in the `conf.Addons` Directory.
- Database files should go into `conf.databases` Directory.
- Environmental variable files should go into `conf.env_variables` Directory.
- Scripts files should go into `conf.scripts` Directory.
- logs, templates, and media files can be found in `conf.miscellaneous` Directory.
- logic that can be used by applications should go into `conf.core` Directory.
- services like file management, emailing etc, should go into `services` Directory.
- All settings are registered in `conf.settings` Directory.

# Deployment Notes:
- Recall that Django only ships along a Developmental server
- besure to use gunicorn as a spark to wsgi  / asgi
- containers are amazing, the project comes shipped with docker.

# Documentation.
- more documentation such as enev sample project flow resides in `docs` folder.

# Useful docker commands
- docker rm $(docker ps -a -q -f status=exited) #remove all containers
- docker rmi -f $(docker images -aq)
- docker build . -t imagename
- docker run imagename
- docker volume rm $(docker volume ls -q) #remove all volumes

# Run into Problems?
Please create an issue if all doesnt go well, thanks.

# Was it helpful?
If this was helpful and resourceful to you, give some `Star` rating.
