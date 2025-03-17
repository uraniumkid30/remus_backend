from django.apps import AppConfig


class MerchantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.merchant"
    def ready(self):
        try:
            from applications.merchant import signals
        except ImportError as err:
            pass
