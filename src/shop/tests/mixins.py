#!/usr/bin/env python
"""Mixins for testing"""

# Standard Library Imports
from contextlib import contextmanager

# Django Library Imports
from django.core.exceptions import ValidationError


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "0.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class ValidationErrorTestMixin(object):
    """Mixin for testing that a ``ValidationError`` is raised for
    particular fields.
    """

    @contextmanager
    def assertModelFieldValidationErrors(
        self, request, expected_error_message_dict
    ):
        """Asserts that a ``ValidationError`` is raised, containing all
        the specified fields, and only the specified fields.

        Comment:
            *   Opted for a mixin rather than `pytest`_ fixture in order
                to make functionality similar to the Django method
                ``assertFormError`` as well as for ease of changing
                testing frameworks if need be.
            *   Method naming is not snake_case as with all other local
                application methods and functions defined in order to be
                consistent with another Django method that performs a
                similar function: ``assertFormError``.

        .. _pytest: https://docs.pytest.org/en/6.2.x/contents.html
        """

        try:
            yield
            raise AssertionError("ValidationError not raised.")

        except ValidationError as e:
            assert expected_error_message_dict == e.message_dict
