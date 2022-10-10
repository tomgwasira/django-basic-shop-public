#!/usr/bin/env python
"""Models for notes associated with other models in Products app."""

# Django Library
from django.db import models

from .product_models import Brand, Category, OptionType, Product, Supplier


__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class AbstractNote(models.Model):
    """Abstract model for implementation of note models."""

    text = models.TextField(max_length=1000, blank=True)
    is_urgent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CategoryNote(AbstractNote):
    """Note for a
    :py:model:`~apps.products.models.product_models.Category`.
    """

    category = models.OneToOneField(Category, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "category"
        verbose_name = "Category Note"
        verbose_name_plural = "Category Notes"

    def __str__(self):
        return f"category-note-{self.category.name}"


class OptionTypeNote(AbstractNote):
    """Note for a
    :py:model:`~apps.products.models.product_models.OptionType`.
    """

    option_type = models.OneToOneField(OptionType, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "option_type"
        verbose_name = "Option Type Note"
        verbose_name_plural = "Option Type Notes"

    def __str__(self):
        return f"option_type-note-{self.option_type.name}"


class BrandNote(AbstractNote):
    """Note for a
    :py:model:`~apps.products.models.product_models.Brand`.
    """

    brand = models.OneToOneField(Brand, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "brand"
        verbose_name = "Brand Note"
        verbose_name_plural = "Brand Notes"

    def __str__(self):
        return f"brand-note-{self.brand.name}"


class SupplierNote(AbstractNote):
    """Note for a
    :py:model:`~apps.products.models.product_models.Supplier`.
    """

    supplier = models.OneToOneField(Supplier, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "supplier"
        verbose_name = "Supplier Note"
        verbose_name_plural = "Supplier Notes"

    def __str__(self):
        return f"supplier-note-{self.supplier.name}"


class ProductNote(AbstractNote):
    """Note for a
    :py:model:`~apps.products.models.product_models.Product`.
    """

    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = "product"
        verbose_name = "Product Note"
        verbose_name_plural = "Product Notes"

    def __str__(self):
        return f"product-note-{self.product.name}"
