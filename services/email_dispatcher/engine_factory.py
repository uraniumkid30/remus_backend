from services.email_dispatcher.django_email_engine import (
    EmailEngine,
    DjangoEmailEngine,
    
)
from services.email_dispatcher.sentinel_email_engine import (
    SentinelEmailEngine
)
from services.email_dispatcher.aws_email_engine import (
    AWSSESEmailEngine,
)


def email_engine_factory(engine_name: str = "DJANGO") -> EmailEngine:
    email_engine_options = {
        "DJANGO": DjangoEmailEngine,
        "AWSSES": AWSSESEmailEngine,
        "SENTINEL": SentinelEmailEngine,
    }
    if email_engine_options.get(engine_name):
        return email_engine_options.get(engine_name)
    raise f"Invalid Email engine name {engine_name}, choose from {list(email_engine_options.keys())}"
