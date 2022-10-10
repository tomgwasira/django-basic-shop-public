from cProfile import label
from django.apps import AppConfig


class ContactDetailsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "contact_details"
    name = "apps.contact_details"
    namespace = "contact_details"
