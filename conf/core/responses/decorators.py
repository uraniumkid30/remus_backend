def enhance_parameters(function):
    def wrapper(*args, **kwargs):
        if len(args) > 1:
            args = (args[0], str(args[1]).upper())
        elif kwargs.get("option"):
            options = kwargs.pop("option")
            kwargs["option"] = str(options).upper()
        return function(*args, **kwargs)

    return wrapper
