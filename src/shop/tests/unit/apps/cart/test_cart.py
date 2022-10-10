#!/usr/bin/env python
"""Tests for views of *Cart* app."""

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
    CategoryFactory,
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
class TestCartSummaryView:
    """Tests for
    :py:class:`~apps.cart.cart.Cart` and
    :py:class:`~apps.cart.views.CartActionView`"""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database.

        Note:
            Value of
            :py:attr:`~apps.products.models.product_models.ProductVariant.stock`
            is defined to be a specific value to ensure that
            :py:class:`~tests.factories.products.product_models_factories.ProductVariantFactory`
            does not accidentally set it to 0.
            This is important because the requests performed in the
            tests require manipulations of the stock.
        """
        # TODO: Remove product
        # TODO: Remove SKU codes
        product = ProductFactory()
        self.product_variant_1 = ProductVariantFactory.create(
            product=product, sku_no="ABC", stock=10
        )
        self.product_variant_2 = ProductVariantFactory.create(
            product=product, sku_no="DEF", stock=10
        )


@pytest.mark.django_db
class TestCart:
    """Tests for
    :py:class:`~apps.cart.cart.Cart` and
    :py:class:`~apps.cart.views.CartActionView`"""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database.

        Note:
            Value of
            :py:attr:`~apps.products.models.product_models.ProductVariant.stock`
            is defined to be a specific value to ensure that
            :py:class:`~tests.factories.products.product_models_factories.ProductVariantFactory`
            does not accidentally set it to 0.
            This is important because the requests performed in the
            tests require manipulations of the stock.
        """
        # TODO: Remove product
        # TODO: Remove SKU codes
        product = ProductFactory()
        self.product_variant_1 = ProductVariantFactory.create(
            product=product, sku_no="ABC", stock=10
        )
        self.product_variant_2 = ProductVariantFactory.create(
            product=product, sku_no="DEF", stock=10
        )

    # ---
    # Add
    # ---
    def test_simple_add_cart_item(self, client):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        successfully adds a cart item and returns expected response.
        """
        item_quantity = 2  # arbitrary quantity to add to cart

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity,
                "action": "add_cart_item",
            },
        )

        assert response.status_code == 200
        assert response.json()["cart_quantity"] == item_quantity
        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(item_quantity),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            }
        }

    def test_complex_add_cart_items(self, client):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        successfully adds multiple cart items and returns expected
        response.

        For this test, a complex sequence of cart add requests is
        performed with the intention of testing that:
            1. The same item can be added to the cart twice.
            2. Multiple items can be added to the cart.
            3. Cart add actions can be interleaved successfully.
        """
        # Arbitrary quantitities to add to cart
        item_quantity_1_first = 3
        item_quantity_2_first = 2
        item_quantity_2_second = 1
        item_quantity_1_second = 2
        item_quantity_2_third = 6

        # Add items to cart using multiple POST requests
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_1_first,
                "action": "add_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_first,
                "action": "add_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_second,
                "action": "add_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_1_second,
                "action": "add_cart_item",
            },
        )

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_third,
                "action": "add_cart_item",
            },
        )

        assert response.status_code == 200
        assert response.json()["cart_quantity"] == (
            item_quantity_1_first
            + item_quantity_1_second
            + item_quantity_2_first
            + item_quantity_2_second
            + item_quantity_2_third
        )
        assert (
            response.json()["cart_quantity"]
            == item_quantity_1_first
            + item_quantity_1_second
            + item_quantity_2_first
            + item_quantity_2_second
            + item_quantity_2_third
        )
        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(
                    item_quantity_1_first + item_quantity_1_second
                ),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            },
            str(self.product_variant_2.id): {
                "item_quantity": str(
                    item_quantity_2_first
                    + item_quantity_2_second
                    + item_quantity_2_third
                ),
                "selling_price": str(self.product_variant_2.selling_price),
                "sku_no": self.product_variant_2.sku_no,
            },
        }

    def test_unsuccessful_simple_add_cart_item_when_item_quantity_above_stock(
        self, client
    ):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        fails to adds a cart item and returns expected response when
        item quantity is above stock.
        """
        item_quantity = 20  # arbitrary quantity, above ProductVariant stock, to add to cart

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity,
                "action": "add_cart_item",
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Failed to add to cart. Total item quantity cannot be greater than stock."
        )
        assert response.json()["cart_quantity"] == 0
        assert client.session.get("cart_session_data") == {}

    def test_unsuccessful_multiple_add_cart_item_when_item_quantity_goes_above_stock_in_second_add(
        self, client
    ):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        fails to adds a cart item and returns expected response when
        item quantity is above stock.

        For this test, the item is added to the cart twice and the
        total quantity only goes above the stock in the second add.
        """
        item_quantity_first = 2
        item_quantity_second = 9

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_first,
                "action": "add_cart_item",
            },
        )

        assert response.status_code == 200

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_second,
                "action": "add_cart_item",
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Failed to add to cart. Total item quantity cannot be greater than stock."
        )
        assert response.json()["cart_quantity"] == item_quantity_first
        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(item_quantity_first),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            }
        }

    # ------
    # Update
    # ------
    def test_simple_update_cart_item(self, client):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        successfully updates a cart item and returns expected response.
        """
        item_quantity_add = 1
        item_quantity_update = 2

        # Add cart item
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_add,
                "action": "add_cart_item",
            },
        )

        # Update cart item
        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_update,
                "action": "update_cart_item",
            },
        )

        assert response.status_code == 200
        assert response.json()["cart_quantity"] == item_quantity_update
        assert response.json()["cart_quantity"] == item_quantity_update
        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(item_quantity_update),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            }
        }

    def test_complex_update_cart_items(self, client):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        successfully updates multiple cart items and returns expected
        response.

        For this test, a complex sequence of cart update requests is
        performed with the intention of testing that:
            1. The same cart item can be updated twice.
            2. Items in a cart with more than one item can be updated.
            3. Cart updated actions can be interleaved successfully.
        """
        # Arbitrary quantitities to add and update cart
        item_quantity_1_add = 7
        item_quantity_2_add = 5
        item_quantity_1_update_first = 3
        item_quantity_2_update_first = 2
        item_quantity_2_update_second = 1
        item_quantity_1_update_second = 2
        item_quantity_2_update_third = 6

        # Add cart items
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_1_add,
                "action": "add_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_add,
                "action": "add_cart_item",
            },
        )

        # Update multiple cart items using multiple POST requests
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_1_update_first,
                "action": "update_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_update_first,
                "action": "update_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_update_second,
                "action": "update_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_1_update_second,
                "action": "update_cart_item",
            },
        )

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_update_third,
                "action": "update_cart_item",
            },
        )

        assert response.status_code == 200
        assert (
            response.json()["cart_quantity"]
            == item_quantity_1_update_second + item_quantity_2_update_third
        )

        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(item_quantity_1_update_second),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            },
            str(self.product_variant_2.id): {
                "item_quantity": str(item_quantity_2_update_third),
                "selling_price": str(self.product_variant_2.selling_price),
                "sku_no": self.product_variant_2.sku_no,
            },
        }

    def test_unsuccessful_simple_update_cart_item_when_item_quantity_above_stock(
        self, client
    ):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        fails to update a cart item and returns expected response when
        item quantity is above stock.
        """
        item_quantity_add = 1
        item_quantity_update = 11

        # Add cart item
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_add,
                "action": "add_cart_item",
            },
        )

        # Update cart item
        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_update,
                "action": "update_cart_item",
            },
        )

        assert response.status_code == 403
        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Failed to update cart item. Total item quantity cannot be greater than stock."
        )
        assert response.json()["cart_quantity"] == item_quantity_add
        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(item_quantity_add),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            },
        }

    def test_unsuccessful_multiple_update_cart_item_when_item_quantity_goes_above_stock_in_second_add(
        self, client
    ):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        fails to update a cart item and returns expected response when
        item quantity is above stock.

        For this test, the item is update twice and the total quantity
        only goes above the stock in the second add.
        """
        item_quantity_add = 2
        item_quantity_update_first = 2
        item_quantity_update_second = 11

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_add,
                "action": "add_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_update_first,
                "action": "update_cart_item",
            },
        )

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_update_second,
                "action": "update_cart_item",
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Failed to update cart item. Total item quantity cannot be greater than stock."
        )

        # Didn't update so item_quantity_update_first
        assert response.json()["cart_quantity"] == item_quantity_update_first
        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(item_quantity_update_first),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            }
        }

    def test_unsuccessful_simple_update_cart_item_when_item_not_found_in_cart(
        self, client
    ):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        fails to update a cart item and returns expected response when
        item is not found in cart.
        """
        item_quantity_update = 11

        # Update cart item that hasn't been added
        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_update,
                "action": "update_cart_item",
            },
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Item not found in cart."
        assert response.json()["cart_quantity"] == 0
        assert client.session.get("cart_session_data") == {}

    # ------
    # Delete
    # ------
    def test_simple_delete_cart_item(self, client):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        successfully deletes a cart item and returns expected response.
        """
        item_quantity_add = 1

        # Add cart item
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_add,
                "action": "add_cart_item",
            },
        )

        # Delete cart item
        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "action": "delete_cart_item",
            },
        )

        assert response.status_code == 200
        assert response.json()["cart_quantity"] == 0
        assert client.session.get("cart_session_data") == {}

    def test_complex_delete_cart_items(self, client):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        successfully updates multiple cart items and returns expected
        response.

        For this test, a complex sequence of cart update requests is
        performed with the intention of testing that:
            1. The same cart item can be updated twice.
            2. Items in a cart with more than one item can be updated.
            3. Cart updated actions can be interleaved successfully.
        """
        # Arbitrary quantitities to add and update cart
        item_quantity_1_add = 7
        item_quantity_2_add = 5

        # Add cart items
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_1_add,
                "action": "add_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_add,
                "action": "add_cart_item",
            },
        )

        # Delete cart items
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "action": "delete_cart_item",
            },
        )

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "action": "delete_cart_item",
            },
        )

        assert response.status_code == 200
        assert response.json()["cart_quantity"] == 0
        assert client.session.get("cart_session_data") == {}

    def test_delete_cart_items_unsuccessful_when_attempting_to_delete_same_item_twice(
        self, client
    ):
        """Tests that :py:class:`~apps.cart.views.CartActionView`
        fails to delete the same item for a second time and returns
        expected response.
        """
        # Arbitrary quantitities to add and update cart
        item_quantity_1_add = 1
        item_quantity_2_add = 1

        # Add cart items
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_1.id,
                "item_quantity": item_quantity_1_add,
                "action": "add_cart_item",
            },
        )

        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "item_quantity": item_quantity_2_add,
                "action": "add_cart_item",
            },
        )

        # Delete cart items
        client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "action": "delete_cart_item",
            },
        )

        response = client.post(
            reverse("cart:cart_action"),
            {
                "product_variant_id": self.product_variant_2.id,
                "action": "delete_cart_item",
            },
        )

        assert response.status_code == 404
        assert response.json()["cart_quantity"] == 1
        assert response.json()["message"] == "Item not found in cart."
        assert client.session.get("cart_session_data") == {
            str(self.product_variant_1.id): {
                "item_quantity": str(item_quantity_1_add),
                "selling_price": str(self.product_variant_1.selling_price),
                "sku_no": self.product_variant_1.sku_no,
            }
        }
