"""`_Pytest`_ fixtures for tests related to *Products* app.

.. _Pytest: https://docs.pytest.org/en/6.2.x/
"""

# Standard library imports
import pathlib

# Django library imports
from django.contrib.auth.models import User
from django.core.management import call_command

# Third party library imports
import pytest

from apps.products.models.product_models import *


@pytest.fixture(scope="class")
def products_db_setup(django_db_setup, django_db_blocker):
    """Loads data fixture for tables in *Products* app."""

    with django_db_blocker.unblock():  # allows specific code paths to have access to database
        file = (
            pathlib.Path(__file__).parent.parent.resolve()
            / "apps/products/fixtures/products.json"
        )
        call_command("loaddata", file)
