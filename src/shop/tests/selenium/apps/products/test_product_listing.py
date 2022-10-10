#!/usr/bin/env python
"""Tests for views of *Products* app."""

# Django library imports
from django.db.models import Q

# Third-party library imports
import pytest

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Local application imports
from tests.factories.products.product_models_factories import *

__author__ = "Thomas Gwasira"
__date__ = "October 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class TestProductListingPage:
    """Tests for the product listing page."""

    pytestmark = [pytest.mark.selenium, pytest.mark.django_db]

    @pytest.fixture(autouse=True)
    def setup_test_env(self, chrome_browser_instance, products_db_setup):
        """Sets up test environment."""
        self.browser = chrome_browser_instance

    def test_category_filtering(
        self,
        live_server,
    ):
        """Tests that clicking on a
        :py:model:`~apps.products.models.product_models.Category`
        on the navbar results in filtering by
        :py:model:`~apps.products.models.product_models.Category`.

        Todo:
            * If a certain depth is not displayed on dropdown, check
                for that case in `for` loop.
        """
        # Get main Category
        main_category = Category.objects.filter(depth=1).first()

        for category in main_category.get_children():
            # Load products page to allow selection of Category
            self.browser.get(("%s%s" % (live_server.url, "/products/")))

            # Store names of all products for that Category
            product_names = []
            [
                product_names.append(product.name)
                for product in category.products.all()
            ]

            # Click the main Category which is the previous Category's parent
            # TODO: Consider hover so that click filters by parent as well
            self.browser.find_element(
                By.XPATH, f"//*[contains(text(), '{main_category.name}')]"
            ).click()

            # Click the Category of interest
            self.browser.find_element(
                By.XPATH, f"//*[contains(text(), '{category.name}')]"
            ).click()

            if len(category.products.all()) == 0:
                assert "No products are available." in self.browser.page_source

            # Assert that all and only Products asociated with Category are displayed
            else:
                product_elements = self.browser.find_elements(
                    By.CLASS_NAME, "product-name"
                )

                for product_element in product_elements:
                    assert product_element.text in product_names

    def test_goes_to_product_detail_page_on_product_click(self, live_server):
        """Tests that clicking on a
        :py:model:`~apps.products.models.product_models.Product` on the
        product listing page results in the
        :py:model:`~apps.products.models.product_models.Product`'s
        product detail page.
        """
        self.browser.get(("%s%s" % (live_server.url, "/products/")))

        product = (
            Product.objects.all().first()
        )  # first Product on product listing page

        # Select first Product on the page
        self.browser.find_element(
            By.XPATH, f"//*[contains(text(), '{product.name}')]"
        ).click()

        # Assert that Product's OptionValues are on resulting page
        option_types = product.option_types.all()
        for option_type in option_types:
            assert f"{option_type.name}" in self.browser.page_source

        assert "Add to Cart" in self.browser.page_source


class TestProductDetailPage:
    """Tests for the product detail page."""

    pytestmark = [pytest.mark.selenium, pytest.mark.django_db]

    @pytest.fixture(autouse=True)
    def setup_test_env(self, chrome_browser_instance, products_db_setup):
        """Sets up test environment."""
        self.browser = chrome_browser_instance

    def test_option_value_selection(
        self,
        live_server,
    ):
        """Tests that clicking on an
        :py:model:`~apps.products.models.product_models.OptionValue`
        button results in correct enabling and disabling of other
        :py:model:`~apps.products.models.product_models.OptionValue`
        buttons
        """
        product = Product.objects.all().first()

        options = []
        for option_type in self.product.option_types.all():
            option_values = OptionValue.objects.filter(
                Q(option_type=option_type)
                & Q(product_variants__product=self.product)
            ).distinct()  # don't re-add duplicate OptionValues

            options.append(
                {"option_type": option_type, "option_values": option_values}
            )

     selected_options = json.loads(request.GET.get("selected_options"))

            # Store all selected OptionValues' ids in list
            option_value_ids = []
            for option_type_name in selected_options:
                option_value_ids.append(
                    int(selected_options[option_type_name]["option_value_id"])
                )

            # Get ProductVariants of current Product with stock >= 0
            product_variants = ProductVariant.objects.filter(
                Q(product__id=product_id) & Q(stock__gt=0)
            )

            # Filter, further, ProductVariants having all the selected OptionValues
            # Using the aggregation approach
            product_variants = (
                product_variants.filter(option_values__id__in=option_value_ids)
                .annotate(num_option_values=Count("option_values"))
                .filter(num_option_values=len(option_value_ids))
            )

            # Initialise cart to compute perceived stock
            cart = Cart(request)

            product_variants_data = []
            available_option_values_data = {}
            for product_variant in product_variants:
                perceived_stock = (
                    product_variant.stock
                )  # value of stock to be used in managing ProductVariants. Not the true stock.

                # If ProductVariant is already in cart, value of stock used should
                # be reduced by the quantity in the cart
                if cart.cart_data["cart_items"].get(str(product_variant.id)):
                    perceived_stock = perceived_stock - int(
                        cart.cart_data["cart_items"][str(product_variant.id)][
                            "item_quantity"
                        ]
                    )

                # Make list of ids of filtered ProductVariants since whole objects can't be
                # passed as JSON
                product_variants_data.append(
                    {
                        "product_variant_id": product_variant.id,
                        "perceived_stock": perceived_stock,
                    }
                )

                # Make collection of all OptionValues of available ProductVariants
                # Collection is dict with key being the id and value being the OptionValue name
                # Will be used by JavaScript to enable OptionValue buttons
                # Not handling any issues to do with hierachy of OptionTypes here
                for option_value in product_variant.option_values.all():
                    # Don't include currently selected OptionValues in list of available
                    # OptionValues. Better performance as JS will not need to select these
                    # OptionValue buttons for possible enabling.
                    if option_value.id not in option_value_ids:
                        available_option_values_data[
                            option_value.id
                        ] = option_value.name

            # Return JSON response
            return JsonResponse(
                {
                    "product_variants_data": product_variants_data,
                    "available_option_values_data": available_option_values_data,
                }
            )
