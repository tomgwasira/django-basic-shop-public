#!/usr/bin/env python
"""Views for Products app."""

# Standard library imports
import json

from itertools import chain, product
import time

# Django library imports
from django.core import paginator
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView, DetailView

# Django REST framework imports
from rest_framework import generics

# Local application imports
from shop.constants import PRODUCTS_PER_PAGE
from .models.image_models import ProductImage
from .models.product_models import (
    Category,
    OptionType,
    OptionValue,
    Product,
    ProductVariant,
)

from apps.cart.cart import Cart


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class ProductListingAllView(ListView):
    """View for product listing (catalogue) page when a
    :py:model:`~apps.products.models.product_models.Category` is not
    specified.

    This gives all the products in the database.

    Todo:
        Replace this with a product showcase or some other type of
        landing page.
    """

    model = Product
    template_name = "products/product_listing.html"
    context_object_name = "products"
    paginate_by = PRODUCTS_PER_PAGE


class ProductListingByCategoryView(ListView):
    """View for product listing (catalogue) page when a
    :py:model:`~apps.products.models.product_models.Category` is
    specified.
    """

    template_name = "products/product_listing.html"
    context_object_name = "products"
    paginate_by = PRODUCTS_PER_PAGE

    def get_queryset(self):
        """Returns
        :py:model:`~apps.products.models.product_models.Product`s having
        given :py:model:`~apps.products.models.product_models.Category`
        or any of its descendents as one of the
        :py:model:`~apps.products.models.product_models.Product`'s
        :py:attr:`~apps.products.models.product_models.Product.categories`.
        """
        # Make list of Category and its descendants
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        query_categories = list(self.category.get_descendants())
        query_categories.append(self.category)

        # Obtain all products with specified Category or its descendants
        products = Product.objects.filter(categories__in=query_categories)

        return products

    def get_context_data(self, **kwargs):
        """Adds the current category to the context."""

        context = super().get_context_data(**kwargs)

        context["category"] = self.category

        return context


class ProductDetailView(DetailView):
    """View for product detail page.

    This gives a
    :py:model:`~apps.products.models.product_models.Product`
    corresponding to a particular slug.
    """

    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_object(self):
        """Returns
        :py:model:`~apps.products.models.product_models.Product` object
        with slug corresponding to requested URL.
        """
        self.product = get_object_or_404(Product, slug=self.kwargs["slug"])
        return self.product

    def get_context_data(self, **kwargs):
        """Adds extra information about queried
        :py:model:`~apps.products.models.product_models.Product` object
        to the context.

        The added context variables are as follows:
            *   ``options``: A nested data structure defined as follows:
                    options = [
                        {
                            "option_type": :py:model:`~apps.products.models.product_models.OptionType`,
                            "option_values": list<:py:model:`~apps.products.models.product_models.OptionValue`>,
                            }
                        },
                        ...
                    ]
                    Order of the list is determined by
                    :py:attr:`~apps.products.models.product_models.OptionType.index`.

        Comment:
            The goal with this view is to have a user select a
            :py:model:`~apps.products.models.product_models.ProductVariant`
            object and the ideal approach (from a programming) perspective
            would have been to list, on the page, all the
            :py:model:`~apps.products.models.product_models.ProductVariant`
            objects corresponding to the queried
            :py:model:`~apps.products.models.product_models.Product`
            object. However, this would be terrible for user experience
            and the better approach is to list some options which the user
            can select where the combination of the selected options results
            in a
            :py:model:`~apps.products.models.product_models.ProductVariant`
            selection. This is why a set of options is added to the context.

        Todo:
            *   Sort out formatting of the nested data structure so that it
            displays nicely on docs.
        """

        context = super().get_context_data(**kwargs)

        # Add to context, all images without OptionValues. These will be displayed everytime, regardless of what
        # OptionValue is selected
        context[
            "product_images_no_option_values"
        ] = ProductImage.objects.filter(
            Q(product=self.product) & Q(option_value__isnull=True)
        )

        # Id of OptionValue to be pre-selected when template page loads
        # Need it to be empty string because when template variable is accessed by javascript, it will
        # be a string so None will actually be the string "None" and so check for if it is not null
        # actually wont work. Also, None is Python. Empty string is the most consistent between both
        # languages.
        context["preselected_option_value_id"] = ""

        # Make Options data structure (discussed in docstring) for current Product
        options = []

        for option_type in self.product.option_types.all():
            option_values = OptionValue.objects.filter(
                Q(option_type=option_type)
                & Q(product_variants__product=self.product)
            ).distinct()  # don't re-add duplicate OptionValues

            # Attach ProductImages to corresponding OptionValues
            option_value_items = []
            for option_value in option_values:
                # Set the very first OptionValue to be dispalyed to be pre-selected when template page loads
                if not context["preselected_option_value_id"]:
                    context["preselected_option_value_id"] = option_value.id

                option_value_items.append(
                    {
                        "option_value": option_value,
                        "product_images": ProductImage.objects.filter(
                            Q(product=self.product)
                            & Q(option_value=option_value)
                        ),
                    }
                )

            options.append(
                {
                    "option_type": option_type,
                    "option_value_items": option_value_items,
                }
            )

        context["options"] = options

        # If Product has no OptionTypes
        # (implying only one ProductVariant for the Product), add extra context
        # variable with id of ProductVariant
        # Gives data structure similar to what would be obtained if
        # OptionValueSelectionView was used
        #
        # get() raises DoesNotExist and MultipleObjectsReturned exceptions
        if not options:
            no_options_product_variant = get_object_or_404(
                ProductVariant, product=self.product
            )

            # Initialise cart to compute perceived stock
            cart = Cart(self.request)

            # If ProductVariant is already in cart, value of stock used should
            # be reduced by the quantity in the cart
            perceived_stock = no_options_product_variant.stock
            if cart.cart_data["cart_items"].get(
                str(no_options_product_variant.id)
            ):
                perceived_stock = no_options_product_variant.stock - int(
                    cart.cart_data["cart_items"][
                        str(no_options_product_variant.id)
                    ]["item_quantity"]
                )

            context["no_options_product_variants_data"] = {
                "product_variant_id": no_options_product_variant.id,
                "perceived_stock": perceived_stock,
            }

        return context


class OptionValueSelectionView(View):
    """View for handling of selection of an
    :py:model:`~apps.products.models.product_models.OptionValue`
    on the product detail page.
    """

    # TODO: Ensure that this is not changing state.
    def get(self, request):
        """Queries the database for all
        :py:model:`~apps.products.models.product_models.ProductVariant`s
        with
        :py:model:`~apps.products.models.product_models.OptionValue`s
        matching selected combination of
        :py:model:`~apps.products.models.product_models.OptionValue`s
        and returns a JSONResponse containing the list of the
        :py:model:`~apps.products.models.product_models.ProductVariant`
        ids among other things.

        Returns:
            JSONResponse: If successful ProductVariant ids, perceived stock

        Warning:
            This should never change state!!!
            Computing ``perceived_stock`` entails using the mutable
                dictionary :py:class`~apps.cart.cart.Cart.cart_items`
                instead of a copy of the dictionary (for better performance);
                therefore caution is required to not alter values in this
                dictionary.
        """
        # TODO: Make flow diagram of the whole perceived stock deal. And just how this generally works.
        if request.GET.get("action") == "option_value_selection":
            # Get information from request data
            product_id = int(request.GET.get("product_id"))
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

        return JsonResponse({})


# # ---------
# # API Views
# # ---------
# class ProductListingAllAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
