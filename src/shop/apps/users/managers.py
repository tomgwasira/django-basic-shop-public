#!/usr/bin/env python
"""Model managers for *Users* app."""

# Django library imports
from django.contrib.auth.base_user import BaseUserManager


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class BaseUserCustomManager(BaseUserManager):
    """:py:model:`~apps.users.models.BaseUser` model manager.

    There are four levels of user power defined in the current version
    of the shop:
        * Customer user: An ordinary user with no power to view or
            alter the backend.
        * Staff user: A user with power to view some features of the
            backend.
        * Admin user: A user with power to alter some features of the
            backend.
        * Superuser: A user with power to alter all features of the
            backend.
    """

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a regular user with the given email and
        password.

        Warning:
            Do not set any ``extra_fields`` here because this method
            is called by the other methods which create a user, therefore,
            setting any fields here would imply overriding the ones
            set before.
        """

        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)

        # Create and save user object
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_customer_user(self, email, password, **extra_fields):
        """Creates and saves a customer user with the given email
        and password."""
        extra_fields.setdefault("is_customer", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_administrator", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_customer") is not True:
            raise ValueError("Customer user must have is_customer=True.")

        return self.create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password, **extra_fields):
        """Creates and saves a regular staff user with the given email
        and password."""
        extra_fields.setdefault("is_customer", False)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_administrator", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff user must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)

    def create_administrator_user(self, email, password, **extra_fields):
        """Creates and saves an administrator user with the given email and
        password."""
        extra_fields.setdefault("is_customer", False)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_administrator", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Admin user must have is_staff=True."))
        if extra_fields.get("is_administrator") is not True:
            raise ValueError("Admin user must have is_administrator=True.")

        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a superuser with the given email and
        password."""
        extra_fields.setdefault("is_customer", False)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_administrator", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_administrator") is not True:
            raise ValueError("Superuser must have is_administrator=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
