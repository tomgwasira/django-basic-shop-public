#!/usr/bin/env python
""" Tests for signals of products app."""

from django.test import TestCase

from model_bakery import baker

from apps.products.admin import *
from apps.products.models import *


__author__ = "Thomas Gwasira"
__date__ = "October 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class ProductVariantSignalsTests(TestCase):
    """Tests signals sent by ProductVariant model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test database with test objects.

        Run once to set up non-modified data for all class methods.
        """

    def test_sku_object_created_in_pre_save_of_product_variant(self):
        """Tests that an Sku object is created in pre_save of ProductVariant."""

        self.assertEqual(
            len(Sku.objects.all()), 0
        )  # ensure that Sku table is empty

        product_variant = baker.make(
            "products.ProductVariant",
            product_variant_summary={
                "sku_no": "dummy_sku_no",
                "product_name": "dummy_product_name",
                "product_category_name": "dummy_product_category_name",
                "option_values": [],
                "date_created": datetime.datetime.now().strftime("%c"),
            },
        )

        auto_created_sku_object = Sku.objects.get(
            sku_no=product_variant.sku_no
        )

        self.assertEqual(
            product_variant.sku_no, auto_created_sku_object.sku_no
        )
        self.assertEqual(
            product_variant, auto_created_sku_object.product_variant
        )
        self.assertEqual(
            product_variant.product_variant_summary,
            auto_created_sku_object.product_variant_summary,
        )
