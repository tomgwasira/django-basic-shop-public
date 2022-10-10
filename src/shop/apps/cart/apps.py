from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "cart"
    name = "apps.cart"
    namespace = "cart"
