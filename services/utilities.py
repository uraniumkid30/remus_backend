import secrets 

def generate_django_secret_key() -> str:
    token = secrets.token_urlsafe(60)
    return f"django-secure-bit64-{token}"


if __name__ == "__main__":
   print(generate_django_secret_key())