#!/usr/bin/env python
"""models.Models for user profiles."""

# Standard library imports
import uuid

# Django library imports
from django.db import models

# Local application imports
from .user_models import (
    BaseUser,
    AdministratorUser,
    GuestCustomerUser,
    RegisteredCustomerUser,
    StaffUser,
    SuperuserUser,
)


__author__ = "Thomas Gwasira"
__date__ = "January 2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class AbstractUserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CustomerProfile(AbstractUserProfile):
    """Profile for a registered customer on the shop."""

    # Any base user can have a CustomerProfile
    base_user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )

    class Meta:
        order_with_respect_to = "base_user"
        verbose_name = "Registered Customer Profile"
        verbose_name_plural = "Registered Customer Profiles"

    def __str__(self):
        return self.base_user.email


class StaffProfile(AbstractUserProfile):
    """Profile for a general employee on the shop."""

    base_user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, related_name="staff_profile"
    )

    class Meta:
        order_with_respect_to = "base_user"
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"

    def __str__(self):
        return self.base_user.email


class GuestCustomerProfile(AbstractUserProfile):
    """Profile for an anonymous user that performs a guest checkout
    on the shop.

    Note:
        Unlike other user profiles, this profile is linked to a
        :py:model:`~apps.users.models.user_models.GuestCustomerUser`
        which is not a
        :py:model:`~apps.users.models.user_models.BaseUser` proxy model
        and does not have authentication features.

    Todo:
        Test performance of this vs. not even having the GuestCustomerUser
        and just storing the email in the profile. It has been coded this
        way for better consistency with the other models.
    """

    guest_customer_user = models.OneToOneField(
        GuestCustomerUser,
        on_delete=models.CASCADE,
        related_name="guest_customer_profile",
    )

    class Meta:
        order_with_respect_to = "guest_customer_user"
        verbose_name = "Guest Customer Profile"
        verbose_name_plural = "Guest Customer Profiles"

    def __str__(self):
        return self.guest_customer_user.email
