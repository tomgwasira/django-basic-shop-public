#!/usr/bin/env python
"""Tests for user managers defined in
:py:mod:`~apps.users.managers`.
"""

# Django library imports
from django.contrib.auth import get_user_model

# Third-party library imports
import pytest

# Local application imports
from apps.users.managers import *


__author__ = "Thomas Gwasira"
__date__ = "December 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


@pytest.mark.django_db
class TestBaseUserManager:
    """Tests for :py:class:`~apps.users.managers.BaseUserManager`."""

    def test_create_user(self):
        """Tests creation of a normal (not super) user."""
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo"
        )
        assert user.email == "normal@user.com"
        assert not user.is_deleted
        assert not user.is_staff
        assert not user.is_superuser

        try:
            # Username is None for the AbstractUser option
            # Username does not exist for the AbstractBaseUser option
            assert user.username is None
        except AttributeError:
            pass

        with pytest.raises(TypeError):
            User.objects.create_user()
        with pytest.raises(TypeError):
            User.objects.create_user(email="")
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        """Tests creation of a superuser."""
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        assert admin_user.email == "super@user.com"
        assert not admin_user.is_deleted
        assert admin_user.is_staff
        assert admin_user.is_superuser

        try:
            # Username is None for the AbstractUser option
            # Username does not exist for the AbstractBaseUser option
            assert admin_user.username is None
        except AttributeError:
            pass

        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )
