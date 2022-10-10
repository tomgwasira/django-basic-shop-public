#!/usr/bin/env python
"""Views for *Products* app."""

# Django library imports
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

# Local application imports
from .cart import Cart


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class CartSummaryView(TemplateView):
    """View for cart summary page."""

    template_name = "cart/cart_summary.html"
    context_object_name = "cart_summary"

    # def get(self, request, *args, **kwargs):
    #     """Sets the cart page to the empty cart page, if cart
    #     is empty.
    #     """
    #     cart = Cart(request)
    #     cart_length = cart.__len__()

    #     if cart_length == 0:
    #         self.template_name = "cart/empty_cart.html"

    #     return super().get(request, *args, **kwargs)


class CartActionView(View):
    """View for performing cart actions."""

    def post(self, request):
        """Extracts information from AJAX request to perform a cart action
        and makes a call to the appropriate method of the current session's
        :py:class:`~apps.cart.cart.Cart` object to perform the action.

        Returns:
            JsonResponse: JSON dictionary containing either a count of
                number of items in the cart (if cart action is successful)
                or an error message (if cart action is unsuccessful)

        Note:
            :py:class:`~apps.products.views.OptionValueSelectionView` ensures
            that the case where the added item quantity is greater than
            stock does not occur by limiting the quantity input. However,
            an additional check is implemented here the quantity input
            may, for some reason, be removed.
        """

        cart = Cart(request)

        # Add item to cart
        if request.POST.get("action") == "add_cart_item":
            return cart.add_cart_item(
                product_variant_id_str=request.POST.get("product_variant_id"),
                item_quantity_str=request.POST.get("item_quantity"),
            )

        # Update cart item
        elif request.POST.get("action") == "update_cart_item":
            return cart.update_cart_item(
                product_variant_id_str=request.POST.get("product_variant_id"),
                item_quantity_str=request.POST.get("item_quantity"),
            )

        # Delete cart item
        elif request.POST.get("action") == "delete_cart_item":
            return cart.delete_cart_item(
                product_variant_id_str=request.POST.get("product_variant_id")
            )
