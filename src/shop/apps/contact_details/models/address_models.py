#!/usr/bin/env python
"""Models for addresses used throughout the shop."""

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


class AbstractAddress(models.Model):
    """Abstract model for implementation address models."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    town_city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CustomerAddress(AbstractAddress):
    """Address for
    :py:model:`~apps.users.models.user_profile_models.CustomerProfile`.
    """

    customer_profile = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="customer_addresses",
    )
    # Retain address even if not displayed to customer as part of profile
    is_saved_to_profile = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Registered Customer Address"
        verbose_name_plural = "Registered Customer Addresses"

    def __str__(self):
        return f"{self.customer_profile.first_name} {self.customer_profile.last_name}"


class StaffAddress(AbstractAddress):
    """Address for
    :py:model:`~apps.users.models.user_profile_models.StaffProfile`.
    """

    staff_profile = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="staff_addresses",
    )
    is_saved_to_profile = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Staff Address"
        verbose_name_plural = "Staff Addresses"

    def __str__(self):
        return (
            f"{self.staff_profile.first_name} {self.staff_profile.last_name}"
        )


class GuestCustomerAddress(AbstractAddress):
    """Address for
    :py:model:`~apps.users.models.user_profile_models.GuestCustomerProfile`.
    """

    guest_customer_profile = models.ForeignKey(
        GuestCustomerProfile,
        on_delete=models.CASCADE,
        related_name="guest_customer_addresses",
    )

    class Meta:
        verbose_name = "Guest Customer Address"
        verbose_name_plural = "Guest Customer Addresses"

    def __str__(self):
        return f"{self.guest_customer_profile.first_name} {self.guest_customer_profile.last_name}"
