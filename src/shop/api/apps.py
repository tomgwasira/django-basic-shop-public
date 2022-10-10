from cProfile import label
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "api"
    name = "api"
    namespace = "api"
