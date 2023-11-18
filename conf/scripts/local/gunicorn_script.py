import os
wsgi_app = "conf.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 2
# The socket to bind
bind = "0.0.0.0:8000"
# Restart workers when code changes (development only!)
reload = True
# Write access and error info to /var/log
gunicorn_dir = os.environ.get("GUNICORN_DIR", "")
accesslog = errorlog = os.path.join(gunicorn_dir, "LOGS", "gunicorn.log")
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = os.path.join(gunicorn_dir, "GUNICORN", "gunicorn.pid")
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
