#!/usr/bin/env python
"""Models for images associated with models in the **products** app."""

# Standard library
from decimal import Decimal

# Django library
# Django library imports
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BooleanField, TextField
from django.db.models.fields.files import ImageField

# Local application library
from shop import constants

# Local application imports
from .product_models import Category, OptionValue, Product, ProductVariant

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class CategoryHeroImage(models.Model):
    """Hero image for a
    :py:class:`~apps.products.models.product_models.Category`
    """

    image = models.ImageField(
        help_text=("Upload a category image"),
        upload_to="apps/products/static/products/img/categories",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.DecimalField(
        max_digits=40,
        decimal_places=constants.POSITION_DP,
        default=Decimal(1000000.0),
    )
    alt_text = models.CharField(
        verbose_name="Alternative Text",
        help_text="Please add alternative text",
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        order_with_respect_to = "category"
        verbose_name = "Category Hero Image"
        verbose_name_plural = "Category Hero Images"

    def __str__(self):
        return f"{self.image}"


class ProductImage(models.Model):
    """Image of a
    :py:model:`~apps.products.models.product_models.Product`.
    """

    image = models.ImageField(
        help_text="Upload a product image", upload_to="img/product-images"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    option_value = models.ForeignKey(
        OptionValue, on_delete=SET_NULL, null=True, blank=True
    )
    position = models.DecimalField(
        max_digits=40,
        decimal_places=constants.POSITION_DP,
        default=Decimal(1000000.0),
    )
    alt_text = models.CharField(
        verbose_name="Alternative Text",
        help_text="Please add alternative text",
        max_length=255,
        null=True,
        blank=True,
    )
    is_featured = models.BooleanField(default=False)
    is_option_value_icon = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        order_with_respect_to = "product"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.image}"


class ProductThumbnailImage(models.Model):
    """Image of a
    :py:model:`~apps.products.models.product_models.Product` thumbnail.

    This is separated from the actual ProductImage because it requires a much lower
    resolution and is used in completely different contexts e.g. for product
    listings, cart page etc., you query product thumbnails. Also, this is actually
    good when loading stuff using async functions.

    TODO: Make a base image class to keep code DRY.
    """

    image = models.ImageField(
        help_text="Upload a product image",
        upload_to="img/product-thumbnail-images",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_thumbnail_images",
    )
    option_value = models.ForeignKey(
        OptionValue, on_delete=SET_NULL, null=True, blank=True
    )
    position = models.DecimalField(
        max_digits=40,
        decimal_places=constants.POSITION_DP,
        default=Decimal(1000000.0),
    )
    alt_text = models.CharField(
        verbose_name="Alternative Text",
        help_text="Please add alternative text",
        max_length=255,
        null=True,
        blank=True,
    )
    is_featured = models.BooleanField(default=False)
    is_option_value_icon = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        order_with_respect_to = "product"
        verbose_name = "Product Thumbnail Image"
        verbose_name_plural = "Product Thumbnail Images"

    def __str__(self):
        return f"{self.image}"
