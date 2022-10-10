#!/usr/bin/env python
""" Tests for validators for the Products app."""

# Django Library Imports
from django.test import TestCase

# Local Application Imports
from apps.products.validators import *


__author__ = "Thomas Gwasira"
__date__ = "October 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"



class ProductsValidatorsTests(TestCase):
    def test_validate_price(self):
        """Tests the :py:meth:`apps.products.validators.validate_price` validator."""
        
        with self.assertRaises(ValidationError):
            validate_price(-10)