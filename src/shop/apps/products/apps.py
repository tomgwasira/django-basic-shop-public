from cProfile import label
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "products"
    name = "apps.products"
    namespace = "products"

    def ready(self):
        import shop.signals
        import apps.products.signals
