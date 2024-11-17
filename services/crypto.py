import base64
import random
import string
import uuid

from hashlib import sha256


def generate_member_number():
    return generate_code(16)


def generate_terminal_id():
    return generate_code(6)


def generate_referral_code():
    return generate_code(6)


def generate_code(size=8):
    character_pool = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(character_pool) for _ in range(size))


def generate_email_hash(email):
    alg = sha256()
    alg.update(email.encode())
    return alg.hexdigest()


def generate_phone_number_hash(phone_number):
    alg = sha256()
    alg.update(phone_number.encode())
    return alg.hexdigest()


def base64_encode_uuid(uuid_id):
    utf8_hex = uuid_id.hex.encode('utf-8')
    base64_encoded = base64.b64encode(utf8_hex)
    base64_string = base64_encoded.decode()
    return base64_string


def decode_base64_to_uuid(base64_str):
    base64_bytes = base64_str.encode('utf-8')
    base64_decoded = base64.b64decode(base64_bytes).decode()
    uuid_id = uuid.UUID(base64_decoded)
    return uuid_id


def mask_email(email: str, marker_weight: int = 5) -> str:
    if not email:
        return email
    delimeter = "@"
    email_identifier, email_domain = email.split(delimeter)
    marker = "*" * marker_weight
    return "".join([email_identifier[0], marker, email_identifier[-1], "@", email_domain])
