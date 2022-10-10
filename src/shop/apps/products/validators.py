#!/usr/bin/env python
""" Validators for **products** app."""

# Django Library Imports
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from shop.constants import (
    MAX_PERCENTAGE_DISCOUNT,
    MIN_PERCENTAGE_DISCOUNT,
)

# Local Application Imports


__author__ = "Thomas Gwasira"
__date__ = "October 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


def validate_percentage_discount(percentage_discount):
    """Validates the
    :py:attr:`~apps.products.models.product_models.ProductVariant.percentage_discount`
    field.

    This validator ensures that:
        1.  :py:attr:`~apps.products.models.product_models.ProductVariant.percentage_discount`
            is not below a set minimum.
        1.  :py:attr:`~apps.products.models.product_models.ProductVariant.percentage_discount`
            is not above a set maximum.
    """
    if percentage_discount < MIN_PERCENTAGE_DISCOUNT:
        raise ValidationError(
            f"Percentage discount cannot be less than {MIN_PERCENTAGE_DISCOUNT}"
        )

    if percentage_discount > MAX_PERCENTAGE_DISCOUNT:
        raise ValidationError(
            f"Percentage discount cannot be greater than {MAX_PERCENTAGE_DISCOUNT}"
        )


def validate_product_variant_summary(product_variant_summary):
    """Validates a ``product_variant_summary`` field to ensure that the
    specified value contains the correct keys and that the corresponding
    values for the keys are not blank.

    Note:
        *   Not checking ``option_values`` as this can be left blank.
    """
    validation_errors = []

    if not product_variant_summary.get("sku_no"):
        validation_errors.append(
            ValidationError(
                _(
                    "Ensure that 'sku_no' has been specified in the product variant summary"
                )
            )
        )

    if not product_variant_summary.get("name"):
        validation_errors.append(
            ValidationError(
                _(
                    "Ensure that 'name' has been specified in the product variant summary"
                )
            )
        )

    if not product_variant_summary.get("categories"):
        validation_errors.append(
            ValidationError(
                _(
                    "Ensure that 'categories' have been specified in the product variant summary"
                )
            )
        )

    if not product_variant_summary.get("created_at"):
        validation_errors.append(
            ValidationError(
                _(
                    "Ensure that 'created_at' has been specified in the product variant summary"
                )
            )
        )

    if len(validation_errors) > 0:
        raise ValidationError(validation_errors)

    # if not (
    #     product_variant_summary.get("sku_no")
    #     and product_variant_summary.get("name")
    #     and product_variant_summary.get("categories")
    #     and product_variant_summary.get("created_at")
    # ):
    #     raise ValidationError(
    #         "Ensure that all values in the product variant summary have been specified"
    #     )

    return product_variant_summary
