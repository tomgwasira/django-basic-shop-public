#!/usr/bin/env python
"""Signal handlers for various signals in project."""

# Django library imports
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Local application imports
from apps.products.models.product_models import Category
from apps.users.models import BaseUser
from apps.users.models.user_profile_models import CustomerProfile


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


@receiver(pre_save)
def clean_on_save(sender, instance, *args, **kwargs):
    """Automatically calls `full_clean` when saving all models (with the
    exception of what is excluded in this signal handler).

    This is necessary because the `save` method does not automatically
    call `full_clean` which may be problematic when forgotten if using
    the API.
    """

    # Do not clean
    if isinstance(instance, Session):
        pass

    # elif isinstance(instance, CustomerProfile):
    #     # Cleaning the o2o field base_user causes issues
    #     pass

    elif isinstance(instance, Category):
        # Cleaning root causes issues
        if instance.is_root():
            pass

    # Clean all other models
    else:
        instance.full_clean()
