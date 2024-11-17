from pydantic import ValidationError as PydanticValidationError


class LogoUnavailableError(Exception):
    """Raise exception if engine cant find logo is not available"""

    def __init__(self, logo_name: str):
        message = f"{logo_name} cannot be found available. please check the name"
        super().__init__(message)


class BadConfigurationError(PydanticValidationError):
    """Raise exception if configuration is mission or not correct"""

    def __init__(self, msg: str = ""):
        message = f"A few configurations are missing or incorrect. please Fix.{msg}"
        super().__init__(message)
