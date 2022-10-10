#!/usr/bin/env python
"""Tests for views of *Products* app."""

# Standard library imports
import html
import json

from importlib import import_module

# Django library imports
from django.db.models import Q
from django.urls import reverse

# Third-party library imports
import pytest

from apps.products.models.product_models import *

from tests.factories.products.product_models_factories import (
    OptionTypeFactory,
    OptionValueFactory,
    ProductFactory,
    ProductVariantFactory,
    SupplierFactory,
)

__author__ = "Thomas Gwasira"
__date__ = "October 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


@pytest.mark.django_db
class TestProductListingAllView:
    """Tests for :py:class:`~apps.products.views.ProductListingAllView`"""

    def test_no_products(self, client):
        """Tests the view when there are no
        :py:model:`~apps.products.models.product_models.Product`s.
        """
        response = client.get(reverse("products:product_listing_all"))

        assert response.status_code == 200
        assert b"No products are available." in response.content
        assert list(response.context["products"]) == []

    def test_with_products(self, client, products_db_setup):
        """Tests the view when there are
        :py:model:`~apps.products.models.product_models.Product`s.
        """
        response = client.get(reverse("products:product_listing_all"))

        assert response.status_code == 200
        assert b"All Products" in response.content

        # Expect all Products in context, in order in which they are
        # queried from database
        assert list(response.context["products"]) == list(
            Product.objects.all()
        )


@pytest.mark.django_db
class TestProductListingByCategoryView:
    """Tests for :py:class:`~apps.products.views.ProductListingByCategoryView`"""

    def test_no_products(self, client):
        """Tests the view when there are no
        :py:model:`~apps.products.models.product_models.Product`s.
        """
        # Add test Category with no children
        category = Category.objects.get(pk=1).add_child(
            name="Test Empty Category"
        )

        response = client.get(
            reverse(
                "products:product_listing_by_category",
                kwargs={"slug": "test-empty-category"},
            )
        )

        assert response.status_code == 200
        assert b"No products are available." in response.content
        assert bytes(html.escape(category.name), "utf-8") in response.content
        assert (
            bytes(html.escape(category.description), "utf-8")
            in response.content
        )
        assert list(response.context["products"]) == []

    def test_with_single_category_products(self, client):
        """Tests the view when there are single
        :py:model:`~apps.products.models.product_models.Category`
        :py:model:`~apps.products.models.product_models.Product`s.
        """
        # Add test Category with no children
        category = Category.objects.get(pk=1).add_child(name="Test Category 0")

        # TODO: Remove all arguments except for categories
        product_1 = ProductFactory.create(
            name="To be removed 1",
            slug="to-be-removed-1",
            sku_symbol="ABC",
            categories=[category],
        )
        product_2 = ProductFactory.create(
            name="To be removed 2",
            slug="to-be-removed-2",
            sku_symbol="DEF",
            categories=[category],
        )
        product_3 = ProductFactory.create(
            name="To be removed 3",
            slug="to-be-removed-3",
            sku_symbol="GHI",
            categories=[category],
        )

        response = client.get(
            reverse(
                "products:product_listing_by_category",
                kwargs={"slug": category.slug},
            )
        )

        assert response.status_code == 200
        assert bytes(html.escape(category.name), "utf-8") in response.content
        assert (
            bytes(html.escape(category.description), "utf-8")
            in response.content
        )
        assert list(response.context["products"]) == [
            product_1,
            product_2,
            product_3,
        ]

    def test_with_multi_category_products(self, client):
        """Tests the view when there are multi-
        :py:model:`~apps.products.models.product_models.Category`
        :py:model:`~apps.products.models.product_models.Product`s.
        """
        # Add test Category with no children
        category_1 = Category.objects.get(pk=1).add_child(
            name="Test Category 1"
        )

        category_2 = Category.objects.get(pk=1).add_child(
            name="Test Category 2"
        )

        # TODO: Remove all arguments except for categories
        product_1 = ProductFactory.create(
            name="To be removed 4",
            slug="to-be-removed-4",
            sku_symbol="ABC-4",
            categories=[category_1],
        )
        product_2 = ProductFactory.create(
            name="To be removed 5",
            slug="to-be-removed-5",
            sku_symbol="DEF-5",
            categories=[category_1, category_2],
        )
        product_3 = ProductFactory.create(
            name="To be removed 6",
            slug="to-be-removed-6",
            sku_symbol="GHI-6",
            categories=[category_2],
        )
        product_4 = ProductFactory.create(
            name="To be removed 7",
            slug="to-be-removed-7",
            sku_symbol="GHI-7",
            categories=[category_2, category_1],
        )

        response = client.get(
            reverse(
                "products:product_listing_by_category",
                kwargs={"slug": category_2.slug},
            )
        )

        assert response.status_code == 200
        assert bytes(html.escape(category_2.name), "utf-8") in response.content
        assert (
            bytes(html.escape(category_2.description), "utf-8")
            in response.content
        )
        assert list(response.context["products"]) == [
            product_2,
            product_3,
            product_4,
        ]


@pytest.mark.django_db
class TestProductDetailView:
    """Tests for :py:class:`~apps.products.views.ProductDetailView`"""

    def test_all_content_displayed_and_correct_context(self, client):
        """Tests that all expected content is displayed and the
        context contains correct information.
        """
        product = Product.objects.get(id=1)

        response = client.get(
            reverse(
                "products:product_detail",
                kwargs={"slug": product.slug},
            )
        )

        assert response.status_code == 200

        # Product section of page
        assert bytes(html.escape(product.name), "utf-8") in response.content
        assert (
            bytes(html.escape(product.description), "utf-8")
            in response.content
        )
        assert response.context["product"] == product

        # Options section of page
        # See ProductDetailView for explanation of options
        options = []
        for option_type in product.option_types.all():
            option_values = OptionValue.objects.filter(
                Q(option_type=option_type)
                & Q(product_variants__product=product)
            ).distinct()

            options.append(
                {"option_type": option_type, "option_values": option_values}
            )

        for option in options:
            assert (
                bytes(html.escape(option["option_type"].name), "utf-8")
                in response.content
            )
            for option_value in option["option_values"]:
                assert (
                    bytes(html.escape(option_value.name), "utf-8")
                    in response.content
                )

        # TODO: Order of OptionValues getting messed up
        # assert response.context["options"] == options

    def test_html_elements(self, client):
        """Tests that all expected elements are displayed."""
        product = Product.objects.get(id=1)

        response = client.get(
            reverse(
                "products:product_detail",
                kwargs={"slug": product.slug},
            )
        )

        assert response.status_code == 200

        for option in response.context["options"]:
            for option_value in option["option_values"]:
                assert (
                    bytes(f'id="option-value-btn-{option_value.id}"', "utf-8")
                    in response.content
                )
        assert b'id="item-quantity"' in response.content
        assert b'id="add-cart-item-btn"' in response.content


@pytest.mark.django_db
class TestOptionValueSelectionView:
    """Tests for :py:function:`~apps.products.views.option_value_selection`"""

    def test_option_value_selection(self, client):
        """Tests that
        :py:func:`~apps.products.views.option_value_selection` returns
        expected response for selection of a combination of expected
        :py:model:`~apps.products.models.product_models.OptionValue`s.
        """
        # TODO: Consider parametrizing
        # TODO: Remove arguments and completely delete OptionType
        # TODO: Remove arguments to factories
        # OptionTypes
        option_type_1 = OptionTypeFactory.create(name="Test OptionType 1")
        option_type_2 = OptionTypeFactory.create(name="Test OptionType 2")
        option_type_3 = OptionTypeFactory.create(name="Test OptionType 3")

        # TODO: Remove arguments to factories
        # OptionValues
        option_value_1_1 = OptionValueFactory.create(
            option_type=option_type_1, sku_symbol="ABC"
        )
        option_value_1_2 = OptionValueFactory.create(
            option_type=option_type_1, sku_symbol="DEF"
        )

        option_value_2_1 = OptionValueFactory.create(
            option_type=option_type_2, sku_symbol="GHI"
        )
        option_value_2_2 = OptionValueFactory.create(
            option_type=option_type_2, sku_symbol="JKL"
        )

        option_value_3_1 = OptionValueFactory.create(
            option_type=option_type_3, sku_symbol="MNO"
        )
        option_value_3_2 = OptionValueFactory.create(
            option_type=option_type_3, sku_symbol="PQR"
        )

        product = ProductFactory.create()
        supplier = SupplierFactory(name="Test Supplier")
        product_variant_1 = ProductVariantFactory.create(
            product=product,
            supplier=supplier,
            sku_no="RMV",
            option_values=[
                option_value_1_1,
                option_value_2_1,
                option_value_3_1,
            ],
        )
        product_variant_2 = ProductVariantFactory.create(
            product=product,
            supplier=supplier,
            option_values=[option_value_1_1, option_value_2_2],
        )

        # First selection
        selected_options = {
            option_value_1_1.option_type.name: {
                "option_value_id": option_value_1_1.id,
                "option_value_name": option_value_1_1.name,
                "option_item_pos": option_value_1_1.option_type.index,
            }
        }

        response = client.get(
            reverse("products:option_value_selection"),
            {
                "product_id": str(product.id),
                "selected_options": json.dumps(selected_options),
                "action": "option_value_selection",
            },
        )

        # Check that available_option_values_data contains all expected
        # OptionValue ids
        assert response.json()["product_variants_data"] == [
            {
                "product_variant_id": product_variant_1.id,
                "perceived_stock": product_variant_1.stock,
            },
            {
                "product_variant_id": product_variant_2.id,
                "perceived_stock": product_variant_1.stock,
            },
        ]
        assert response.json()["available_option_values_data"] == {
            f"{option_value_2_1.id}": f"{option_value_2_1.name}",
            f"{option_value_3_1.id}": f"{option_value_3_1.name}",
            f"{option_value_2_2.id}": f"{option_value_2_2.name}",
        }

        # Second selection
        selected_options = {
            option_value_1_1.option_type.name: {
                "option_value_id": option_value_1_1.id,
                "option_value_name": option_value_1_1.name,
                "option_item_pos": option_value_1_1.option_type.index,
            },
            option_value_2_1.option_type.name: {
                "option_value_id": option_value_2_1.id,
                "option_value_name": option_value_2_1.name,
                "option_item_pos": option_value_2_1.option_type.index,
            },
        }

        response = client.get(
            reverse("products:option_value_selection"),
            {
                "product_id": str(product.id),
                "selected_options": json.dumps(selected_options),
                "action": "option_value_selection",
            },
        )

        # Check that available_option_values_data contains all expected
        # OptionValue ids
        assert response.json()["product_variants_data"] == [
            {
                "product_variant_id": product_variant_1.id,
                "perceived_stock": product_variant_1.stock,
            }
        ]

        assert response.json()["available_option_values_data"] == {
            f"{option_value_3_1.id}": f"{option_value_3_1.name}"
        }

    def test_perceived_stock_when_item_added_to_cart_already(self, client):
        """Tests that
        :py:func:`~apps.products.views.option_value_selection` returns
        expected `perceived_stock` when target
        :py:model:`apps.products.models.product_models.ProductVariant`
        has been added to cart already.
        """
        # TODO: Consider parametrizing
        # TODO: Remove arguments and completely delete OptionType
        # TODO: Remove arguments to factories
        # OptionTypes
        option_type = OptionTypeFactory.create(name="Test OptionType 1")

        # TODO: Remove arguments to factories
        # OptionValues
        option_value = OptionValueFactory.create(
            option_type=option_type, sku_symbol="ABC"
        )

        product = ProductFactory.create()
        supplier = SupplierFactory(name="Test Supplier")
        product_variant = ProductVariantFactory.create(
            product=product,
            supplier=supplier,
            sku_no="RMV",
            option_values=[option_value],
        )

        # Add to cart
        item_quantity = 5
        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": product_variant.id,
                "item_quantity": item_quantity,
                "action": "add_cart_item",
            },
        )

        # Selection OptionValue
        selected_options = {
            option_value.option_type.name: {
                "option_value_id": option_value.id,
                "option_value_name": option_value.name,
                "option_item_pos": option_value.option_type.index,
            }
        }

        response = client.get(
            reverse("products:option_value_selection"),
            {
                "product_id": str(product.id),
                "selected_options": json.dumps(selected_options),
                "action": "option_value_selection",
            },
        )

        # Check that available_option_values_data contains all expected
        # OptionValue ids
        assert response.json()["product_variants_data"] == [
            {
                "product_variant_id": product_variant.id,
                "perceived_stock": product_variant.stock - item_quantity,
            },
        ]
        assert response.json()["available_option_values_data"] == {}
