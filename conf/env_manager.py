import os

import environ
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

from conf.addons.directories import (
    ENV_DIR,
)


env = environ.Env()


def env_to_enum(enum_cls, value):
    for x in enum_cls:
        if x.value == value:
            return x

    raise ImproperlyConfigured(
        f"Env value {repr(value)} could not be found in {repr(enum_cls)}"
    )


def get_env_variable(var_name, default=None, strict_mode=False):
    """Get the environment variable or return exception."""
    if not strict_mode:
        return os.environ.get(var_name, default)
    try:
        return os.environ[var_name]
    except KeyError as error:
        error_msg = f"Set the {var_name} environment variable {error}"
        raise ImproperlyConfigured(error_msg)


class DotenvService:
    def __init__(self):
        project_folder = os.path.expanduser(ENV_DIR)
        load_dotenv(os.path.join(project_folder, '.env'))

    def processor(self, action, key, default):
        value = os.getenv(key) or default
        try:
            if value is not None:
                result = action(value)
        except Exception:
            result = None
        finally:
            return result

    def str(self, key, default=None):
        return self.processor(str, key, default)

    def bool(self, key, default=None):
        return self.processor(bool, key, default)

    def int(self, key, default=None):
        return self.processor(int, key, default)

    def float(self, key, default=None):
        return self.processor(float, key, default)

    def list(self, key, default=None):
        return self.processor(list, key, default)


py_env = DotenvService()
