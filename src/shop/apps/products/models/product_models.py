#!/usr/bin/env python
"""Models for the Products app."""

# Standard library
import uuid
from decimal import Decimal

# Django library
from django.db import models
from django.urls import reverse

# Third-party libraries
from django_extensions.db.fields import AutoSlugField
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from treebeard import ns_tree

# Local application library
from shop import constants, routines

__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class Category(ns_tree.NS_Node):
    """Category of a product.

    The database table generated from this class makes uses of the
    `django-treebeard`_ nested set model for a hierachical organisation of
    objects such that categories may have parent and/or children categories.

    .. _django-treebeard: https://django-treebeard.readthedocs.io/en/latest/
    """

    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=True)

    slug = AutoSlugField(
        populate_from="name",
        overwrite=True,
        slugify_function=routines.autoslug_slugify,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        # Ordering automatic

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return a URL for the :py:class:`~apps.products.product_models.Category`
        object.

        Returns:
            str: URL for the
                :py:model:`~apps.products.product_models.Category`.
        """
        return reverse(
            "products:product_listing_by_category", args=[self.slug]
        )

    def get_ancestors_and_self(self):
        """Return list with current
        :py:class:`~apps.products.product_models.Category` object and its
        ancestors.

        Use `django-treebeard`_'s ``get_ancestors`` if you don't
        want to include the current
        :py:class:`~apps.products.product_models.Category` object itself.

        Returns:
            list: List with current
            :py:class:`~apps.products.product_models.Category` object and its
            ancestors.

        .. _django-treebeard: https://django-treebeard.readthedocs.io/en/latest/
        """

        if self.is_root():
            return [self]

        return list(self.get_ancestors()) + [self]

    def get_descendants_and_self(self):
        """Return list with current
        :py:class:`~apps.products.product_models.Category` object and its
        descendants.

        Use `django-treebeard`_'s ``get_ancestors`` if you don't want to
        include the current :py:class:`~apps.products.product_models.Category`.
        object itself.

        Returns:
            list: List with current
            :py:class:`~apps.products.product_models.Category` object and its
            descendants.

        .. _django-treebeard: https://django-treebeard.readthedocs.io/en/latest/
        """
        return self.get_tree(self)

    def get_pk_related_field_data(self):
        return {"pk": self.pk, "name": self.name}


class OptionType(models.Model):
    """Type of a product variation e.g. size, volume etc."""

    name = models.CharField(max_length=250, unique=True)
    display_name = models.CharField(max_length=250, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    position = models.DecimalField(
        max_digits=constants.POSITION_MAX_DIGITS,
        decimal_places=constants.POSITION_DP,
        default=Decimal(1000000.0),
    )
    is_active = models.BooleanField(default=True)

    slug = AutoSlugField(
        populate_from="name",
        overwrite=True,
        slugify_function=routines.autoslug_slugify,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ("position",)
        verbose_name = "Option"
        verbose_name_plural = "Options"

    def __str__(self):
        return self.name

    def get_pk_related_field_data(self):
        return {"pk": self.pk, "name": self.name}


class OptionValue(models.Model):
    """Value of a type of a product variation e.g. small, 100 ml etc."""

    name = models.CharField(max_length=250, verbose_name="Name/ Value")
    display_name = models.CharField(max_length=250, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    option_type = models.ForeignKey(
        OptionType, on_delete=models.CASCADE, related_name="option_values"
    )
    sku_symbol = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        order_with_respect_to = "option_type"
        verbose_name = "Option Value"
        verbose_name_plural = "Option Values"

    def __str__(self):
        return f"{self.name} {self.unit}".strip()

    def get_pk_related_field_data(self):
        return {"pk": self.pk, "name": self.name}


class Brand(models.Model):
    """Brand of a product."""

    name = models.CharField(max_length=250, unique=True)
    position = models.DecimalField(
        max_digits=40,
        decimal_places=constants.POSITION_DP,
        default=Decimal(1000000.0),
    )
    is_active = models.BooleanField(default=True)

    slug = AutoSlugField(
        populate_from="name",
        overwrite=True,
        slugify_function=routines.autoslug_slugify,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ("position",)
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    def get_pk_related_field_data(self):
        return {"pk": self.pk, "name": self.name}


class Supplier(models.Model):
    """Supplier of a product variant."""

    name = models.CharField(max_length=250)
    details = models.TextField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ("name",)
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.name

    def get_pk_related_field_data(self):
        return {"pk": self.pk, "name": self.name}


class ProductType(models.Model):
    """Type of a product."""

    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1000, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ("name",)
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag for a product."""

    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """On save, this method converts all characters in
        :py:attr:`~apps.products.product_models.Tag.name` to lowercase.
        """
        self.name = self.name.lower()

        super(Tag, self).save(*args, **kwargs)


class Product(models.Model):
    """Basic product."""

    ACTIVE = 1
    ARCHIVED = 2
    DELETED = 3

    PRODUCT_STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (ARCHIVED, "Archived"),
        (DELETED, "Deleted"),
    ]

    name = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, blank=True)
    product_types = models.ManyToManyField(
        ProductType, blank=True, related_name="products"
    )
    categories = models.ManyToManyField(
        Category, blank=True, related_name="products"
    )
    brands = models.ManyToManyField(Brand, blank=True, related_name="products")
    option_types = models.ManyToManyField(
        OptionType, blank=True, related_name="products"
    )
    description = models.TextField(blank=True, max_length=1000)
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    sku_symbol = models.CharField(max_length=5)
    status = models.IntegerField(
        choices=PRODUCT_STATUS_CHOICES, default=ACTIVE
    )
    is_active = models.BooleanField(default=True)

    slug = AutoSlugField(
        populate_from="name",
        overwrite=True,
        slugify_function=routines.autoslug_slugify,
        unique=True,
    )
    min_price = MoneyField(
        max_digits=19,
        decimal_places=constants.CURRENCY_DP,
        default_currency=constants.DEFAULT_CURRENCY,
        validators=[MinMoneyValidator(constants.MIN_PRICE)],
    )
    max_price = MoneyField(
        max_digits=19,
        decimal_places=constants.CURRENCY_DP,
        default_currency=constants.DEFAULT_CURRENCY,
        validators=[MinMoneyValidator(constants.MIN_PRICE)],
    )
    min_price_original = MoneyField(
        max_digits=19,
        decimal_places=constants.CURRENCY_DP,
        default_currency=constants.DEFAULT_CURRENCY,
        validators=[MinMoneyValidator(constants.MIN_PRICE)],
    )
    max_price_original = MoneyField(
        max_digits=19,
        decimal_places=constants.CURRENCY_DP,
        default_currency=constants.DEFAULT_CURRENCY,
        validators=[MinMoneyValidator(constants.MIN_PRICE)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ("name",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return a URL for the :py:class:`~apps.products.product_models.Product`
        object.

        Returns:
            str: URL for the
                :py:model:`~apps.products.product_models.Product` object.
        """
        return reverse("products:product_detail", args=[self.slug])


class ProductVariant(models.Model):
    """Variant of a particular product."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_variants"
    )
    option_values = models.ManyToManyField(
        OptionValue, blank=True, related_name="product_variants"
    )
    selling_price = MoneyField(
        max_digits=19,
        decimal_places=constants.CURRENCY_DP,
        default_currency=constants.DEFAULT_CURRENCY,
        validators=[MinMoneyValidator(constants.MIN_PRICE)],
    )
    # do not set to 0 when blank!
    discounted_price = MoneyField(
        max_digits=19,
        decimal_places=constants.CURRENCY_DP,
        default_currency=constants.DEFAULT_CURRENCY,
        null=True,
        blank=True,
        validators=[MinMoneyValidator(constants.MIN_PRICE)],
    )
    stock = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(
        Supplier, blank=True, null=True, on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=True)

    sku_no = models.CharField(max_length=constants.MAX_SKU_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        order_with_respect_to = "product"
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        return self.sku_no
