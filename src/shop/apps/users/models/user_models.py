#!/usr/bin/env python
"""Models for custom users."""

# Standard library imports
import uuid

# Django library imports
from email.policy import default
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import (
    BooleanField,
    DateTimeField,
    EmailField,
)

# Local application imports
from ..managers import BaseUserCustomManager


__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class BaseUser(AbstractBaseUser, PermissionsMixin):
    """A user on the shop.

    This is model is used for authentication and is defined to be the
    :py:const`~shop.settings.AUTH_USER_MODEL`, replacing the built-in
    Django ``User`` model.

    The main reason why the built-in ``User`` model is replaced with
    the current one is because, in this model, the default
    authentication field ``username`` is replaced with
    :py:attr:`~apps.users.models.user_models.email`. Additionally, using
    a custom model for authentication will allow for better scalability,
    say, if the ``REQUIRED_FIELDS`` are to be changed.

    This model has proxy models corresponding to different roles within
    the user roles within the business structure, allowing for different
    different interfaces for the same underlying database model e.g.
    different implementations of the ``save`` method.

    This model has the flags:
        * :py:attr:`~apps.users.models.user_models.is_customer`
        * :py:attr:`~apps.users.models.user_models.is_staff`
        * :py:attr:`~apps.users.models.user_models.is_administrator`
        * :py:attr:`~apps.users.models.user_models.is_superuser`
    which specify the roles of the current user. The Django
    ``AbstractBaseUser`` class which this model inherits from already
    implements the ``is_staff`` and ``is_superuser`` flags which are
    recognised in other built-in functionality such as admin site access.
    The aforementioned proxy models for the various roles set these
    flags as does the
    :py:class:`~apps.users.managers.BaseUserCustomManager`.

    Warning:
        Avoid renaming this model 'User' as that would conflict with
        the built-in ``User`` model if accidentally imported.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = EmailField("email address", unique=True)
    is_customer = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_administrator = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # Set authentication field to email
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    # Specify that all objects for the class come from the BaseUserCustomManager
    objects = BaseUserCustomManager()

    class Meta:
        ordering = ("email",)
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class RegisteredCustomerUser(BaseUser):
    """Proxy model for :py:model:`~apps.users.models.BaseUser` to allow for
    a ``BaseUserAdmin`` dedicated to
    :py:model:`~apps.users.models.MemberCustomerProfile` model.
    """

    class Meta:
        proxy = True
        verbose_name = "Registered Customer"
        verbose_name_plural = "Registered Customers"

    def save(self, *args, **kwargs):
        """Sets :py:attr:`~apps.users.models.BaseUser.is_customer` flag.

        This has to be done in ``save`` method rather than ``pre_save``
        signal as, signals for proxy models are not working.

        This is called is admin of CustomerUserAdmin.
        """
        self.is_customer = True

        return super().save(self, *args, **kwargs)


class StaffUser(BaseUser):
    """Proxy :py:model:`~apps.users.models.BaseUser` model to allow for
    a ``BaseUserAdmin`` dedicated to
    :py:model:`~apps.users.models.StaffProfile` model.
    """

    class Meta:
        proxy = True
        verbose_name = "Staff"
        verbose_name_plural = "All Staff"

    def save(self, *args, **kwargs):
        """Sets :py:attr:`~apps.users.models.BaseUser.is_staff` flag.

        This has to be done in ``save`` method rather than ``pre_save``
        signal as, signals for proxy models are not working.
        """
        self.is_customer = False
        self.is_staff = True

        return super().save(self, *args, **kwargs)


class AdministratorUser(BaseUser):
    """Proxy :py:model:`~apps.users.models.BaseUser` model to allow for
    a ``BaseUserAdmin`` dedicated to.
    """

    class Meta:
        proxy = True
        verbose_name = "Administrator"
        verbose_name_plural = "Administrators"

    def save(self, *args, **kwargs):
        """Sets :py:attr:`~apps.users.models.BaseUser.is_staff` and
        :py:attr:`~apps.users.models.BaseUser.is_administrator` flags.

        This has to be done in ``save`` method rather than ``pre_save``
        signal as, signals for proxy models are not working.
        """
        self.is_customer = False
        self.is_staff = True
        self.is_administrator = True

        return super().save(self, *args, **kwargs)


class SuperuserUser(BaseUser):
    """Proxy :py:model:`~apps.users.models.BaseUser` model to allow for
    a ``BaseUserAdmin``.
    """

    class Meta:
        proxy = True
        verbose_name = "Superuser"
        verbose_name_plural = "Superusers"

    def save(self, *args, **kwargs):
        """Sets :py:attr:`~apps.users.models.BaseUser.is_staff`,
        :py:attr:`~apps.users.models.BaseUser.is_administrator` and
        :py:attr:`~apps.users.models.BaseUser.is_superuser` flags.

        This has to be done in ``save`` method rather than ``pre_save``
        signal as, signals for proxy models are not working.
        """
        self.is_customer = False
        self.is_staff = True
        self.is_administrator = True
        self.is_superuser = True

        return super().save(self, *args, **kwargs)


class GuestCustomerUser(Model):
    """Customer user without any authentication features.

    This model is to be used for anonymous users who perform a guest
    checkout.

    Warning:
        This model is different from the proxy models in this module.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = EmailField("email address")  # not unique
    is_customer = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ("email",)
        verbose_name = "Guest Customer"
        verbose_name_plural = "Guest Customers"

    def __str__(self):
        return self.email


# TODO: !!!!!!!!!!!!!!!!!!!!! USE FLAKE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
# TODO: !!!!!!!!!!!!!! Check that docs are being generated correctly !!!!!!!!11
# TODO: !!!!!!!!!!!!!!!!!!!!! USE ISORT !!!!!!!!!!!!!!!!!!!!!!!!!!!!1
# TODO: !!!!!!!!!!!!!!!!!!!! USE COVERAGE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
