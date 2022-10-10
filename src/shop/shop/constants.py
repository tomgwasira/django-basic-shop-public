#!/usr/bin/env python
"""Constants for use throughout the project.

Todo:
    * Use bit shift for CURRENCY_PRECISION.
"""

# Standard library
# Standard libray imports
from decimal import Decimal

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"

# == General Configuration ============================================
POSITION_MAX_DIGITS = 40


# HOME_URL = reverse("products:product_listing_all")

MAX_SKU_LENGTH = 30  # maximum length of an SKU code
DEFAULT_CURRENCY = "ZAR"  # default currency code for use in django-money
CURRENCY_DP = 2  # number of decimal places for currency
CURRENCY_PRECISION = Decimal(10) ** (
    -1 * CURRENCY_DP
)  # fixed exponent to which money values are rounded
MIN_PRICE = Decimal(0.01).quantize(
    CURRENCY_PRECISION
)  # minimum value of a price field. Price cannot be 0.
PERCENTAGE_DISCOUNT_DP = 1  # number of decimal places for percentage discount
PERCENTAGE_DISCOUNT_PRECISION = Decimal(10) ** (
    -1 * PERCENTAGE_DISCOUNT_DP
)  # fixed exponent to which percentage discount is rounded
MIN_PERCENTAGE_DISCOUNT = Decimal(0.1).quantize(PERCENTAGE_DISCOUNT_PRECISION)
MAX_PERCENTAGE_DISCOUNT = Decimal(90).quantize(PERCENTAGE_DISCOUNT_PRECISION)
MIN_TOTAL = Decimal(0.00).quantize(
    CURRENCY_PRECISION
)  # minimum value of a total field
MIN_COST = Decimal(0.00).quantize(
    CURRENCY_PRECISION
)  # minimum value of a cost field
POSITION_DP = 30

NOTE_PREVIEW_LENGTH = 30  # number of the actual note text that will be used as a preview of the note

PRODUCTS_PER_PAGE = 10

# == Orders ============================================================
# -- Order Payment Statuses --------------------------------------------
