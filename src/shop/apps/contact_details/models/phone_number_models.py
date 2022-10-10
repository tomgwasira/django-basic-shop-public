#!/usr/bin/env python
"""Models for phone numbers used throughout the shop."""

# Standard library imports
import uuid

# Django library imports
from django.db import models

# Local application imports
from apps.users.models.user_profile_models import (
    GuestCustomerProfile,
    CustomerProfile,
    StaffProfile,
)


__author__ = "Thomas Gwasira"
__date__ = "January 2022"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class AbstractPhoneNumber(models.Model):
    """Abstract model for implementation phone number models."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CustomerPhoneNumber(AbstractPhoneNumber):
    """Phone number for
    :py:model:`~apps.users.models.user_profile_models.CustomerProfile`.
    """

    customer_profile = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="customer_phone_numbers",
    )

    class Meta:
        verbose_name = "Registered Customer Phone Number"
        verbose_name_plural = "Registered Customer Phone Numbers"

    def __str__(self):
        return (
            self.customer_profile.first_name + self.customer_profile.last_name
        )


class StaffPhoneNumber(AbstractPhoneNumber):
    """Phone number for
    :py:model:`~apps.users.models.user_profile_models.StaffProfile`.
    """

    staff_profile = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="staff_phone_numbers",
    )

    class Meta:
        verbose_name = "Staff Phone Number"
        verbose_name_plural = "Staff Phone Numbers"

    def __str__(self):
        return (
            f"{self.staff_profile.first_name} {self.staff_profile.last_name}"
        )


class GuestCustomerPhoneNumber(AbstractPhoneNumber):
    """Phone number for
    :py:model:`~apps.users.models.user_profile_models.GuestCustomerProfile`.
    """

    guest_customer_profile = models.ForeignKey(
        GuestCustomerProfile,
        on_delete=models.CASCADE,
        related_name="guest_customer_phone_numbers",
    )

    class Meta:
        verbose_name = "Guest Customer Phone Number"
        verbose_name_plural = "Guest Customer Phone Numbers"

    def __str__(self):
        return (
            self.guest_customer_profile.first_name
            + self.guest_customer_profile.last_name
        )
