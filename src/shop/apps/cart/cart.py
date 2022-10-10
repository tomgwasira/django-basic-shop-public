#!/usr/bin/env python
"""Definition of Cart class."""

# Django library imports
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Local application imports
from apps.products.models.product_models import ProductVariant


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class Cart:
    """The 'cart' for a browsing session.

    This class wraps all the information about the cart (including items
    stored in the cart) as well as methods that can be performed on the
    cart.

    It is created and initialised everytime an HTTP request is made by
    means of the context processor
    :py:func`apps.cart.context_processors.get_cart`.

    Attributes:
        session ('django.contrib.sessions.backends.db.SessionStore'): A
            Django session store object from the corresponding session
            engine.
        cart_items (dict): Dictionary containing, information about the
            :py:class:`apps.products.product_models.ProductVariant`
            objects that have been 'added to the cart'. The structure
            of the dict is as follows:
            cart_items = {
                :py:attr:`~apps.products.models.product_models.ProductVariant.id` (str): {
                    "item_quantity": (str),
                    "selling_price": (str),
                    "sku_no": (str),
                }
                ...
            }

    Todo:
        *   Add discounted_price to the cart_items and use appropriately
            in Cart Summary page or consider doing that in __iter__.
    """

    def __init__(self, request):
        """Constructor method.

        The constructor checks if, for the current browsing session,
        some session data corresponding to a cart is stored. If so, it
        extracts the dictionary and assigns it to ``cart_items``. If not,
        a ``cart_items`` dictionary is created.
        """

        self.session = request.session

        # If cart session exists, use cart data to initialise cart_items attribute
        if "cart_session_data" in self.session:
            self.cart_data = self.session.get("cart_session_data")
            # Set user email if available
            self.cart_data["user"] = getattr(request.user, "email", "")

        # If not, create new cart session and initialise it and cart_data with {}
        else:
            self.cart_data = self.session["cart_session_data"] = {
                "user": getattr(request.user, "email", ""),
                "cart_items": {},
            }

    def save_cart(self):
        """Saves the current cart session information to session
        database."""
        self.session.modified = True

    def add_cart_item(self, product_variant_id_str, item_quantity_str):
        """Adds a :py:model`~apps.products.product_models.ProductVariant`
        item, to the cart.

        This is done by adding the
        :py:attr:`apps.products.product_models.ProductVariant.id` as a
        key to the ``cart_items`` dictionary and information pertaining
        to quantity etc. as a value for the key. The data is then saved
        to the session database.

        This method is called by the view connected to a button by the
        URL 'add_cart_item'.

        Args:
            product_variant_id_str (str): String form of the id of the
            :py:model:`~apps.products.product_models.ProductVariant`
            to be added to the cart.
            item_quantity_str (str): String form of the quantity of the
            item to be added.

        Return:
            JsonResponse: JSON object containing the cart length and the
                HTTP status code of the action as well as an error
                message if the action was unsuccessful
        """

        product_variant = get_object_or_404(
            ProductVariant, id=product_variant_id_str
        )

        # If ProductVariant already in cart, increment the existing item_quantity
        # by the additional item_quantity and reduce perceived stock
        if product_variant_id_str in self.cart_data["cart_items"]:
            updated_item_qty = int(
                self.cart_data["cart_items"].get(product_variant_id_str)[
                    "item_quantity"
                ]
            ) + int(item_quantity_str)

            # If ProductVariant stock is greater than desired quantity add to
            # cart and return True
            if product_variant.stock >= updated_item_qty:
                self.cart_data["cart_items"][product_variant_id_str][
                    "item_quantity"
                ] = str(updated_item_qty)

                self.save_cart()

                return JsonResponse({"cart_quantity": self.__len__()})
            return JsonResponse(
                {
                    "status": "false",
                    "message": "Failed to add to cart. Total item quantity cannot be greater than stock.",
                    "cart_quantity": self.__len__(),
                },
                status=403,
            )

        else:
            # If ProductVariant stock is greater than desired quantity add to
            # cart and return True
            if product_variant.stock >= int(item_quantity_str):
                self.cart_data["cart_items"][product_variant_id_str] = {
                    "item_quantity": item_quantity_str,
                    "selling_price": str(product_variant.selling_price),
                    "sku_no": product_variant.sku_no,
                }

                self.save_cart()

                return JsonResponse({"cart_quantity": self.__len__()})
            return JsonResponse(
                {
                    "status": "false",
                    "message": "Failed to add to cart. Total item quantity cannot be greater than stock.",
                    "cart_quantity": self.__len__(),
                },
                status=403,
            )

    def update_cart_item(self, product_variant_id_str, item_quantity_str):
        """Updates the cart item.

        Args:
            product_variant_id_str (str): String form of the id of the
            :py:model:`~apps.products.product_models.ProductVariant`
            to be added to the cart.
            item_quantity_str (str): String form of the quantity of the
            item to be added.

        Return:
            JsonResponse: JSON object containing the cart length and the
                HTTP status code of the action as well as an error
                message if the action was unsuccessful
        """

        if product_variant_id_str in self.cart_data["cart_items"]:
            product_variant = get_object_or_404(
                ProductVariant, id=product_variant_id_str
            )

            # If ProductVariant stock is greater or equal to desired quantity update
            if product_variant.stock >= int(item_quantity_str):
                self.cart_data["cart_items"][product_variant_id_str][
                    "item_quantity"
                ] = item_quantity_str

                self.save_cart()

                return JsonResponse({"cart_quantity": self.__len__()})
            return JsonResponse(
                {
                    "status": "false",
                    "message": "Failed to update cart item. Total item quantity cannot be greater than stock.",
                    "cart_quantity": self.__len__(),
                },
                status=403,
            )
        return JsonResponse(
            {
                "status": "false",
                "message": "Item not found in cart.",
                "cart_quantity": self.__len__(),
            },
            status=404,
        )

    def delete_cart_item(self, product_variant_id_str):
        """Deletes the cart item.

        Args:
            product_variant_id_str (str): String form of the id of the
            :py:class`apps.products.product_models.ProductVariant`
            to be deleted from the cart.

        Return:
            JsonResponse: JSON object containing the cart length and the
                HTTP status code of the action as well as an error
                message if the action was unsuccessful
        """

        if product_variant_id_str in self.cart_data["cart_items"]:
            del self.cart_data["cart_items"][product_variant_id_str]

            self.save_cart()
            return JsonResponse({"cart_quantity": self.__len__()})
        return JsonResponse(
            {
                "status": "false",
                "message": "Item not found in cart.",
                "cart_quantity": self.__len__(),
            },
            status=404,
        )

    def cart_details(self):
        """Returns a full representation of the cart, with the following
        structure:

        cart_details = {
            "cart_items": [
                {
                    "product_variant": <ProductVariant>,
                    "total_price": <Money>,
                    "item_quantity": <int>,
                }
                ...
            ],
            "cart_total": <Money>
        }

        Returns:
            dict: Dictionary containing full details about the cart and
                objects within it.
        """
        cart_details = {"cart_items": []}
        cart_total = (
            0  # initialise total price of items in cart for accumulation
        )
        cart_length = 0

        # Make full representations of each cart item
        for product_variant_id_str in self.cart_data["cart_items"]:
            product_variant = get_object_or_404(
                ProductVariant, id=int(product_variant_id_str)
            )
            item_quantity = int(
                self.cart_data["cart_items"][product_variant_id_str][
                    "item_quantity"
                ]
            )

            if product_variant.discounted_price:
                total_price = product_variant.discounted_price * item_quantity

            else:
                total_price = product_variant.selling_price * item_quantity

            cart_details["cart_items"].append(
                {
                    "product_variant": product_variant,
                    "total_price": total_price,
                    "item_quantity": item_quantity,
                }
            )

            cart_total += total_price
            cart_length += 1
        cart_details["cart_total"] = cart_total
        cart_details["cart_length"] = cart_length

        return cart_details

    def __len__(self):
        """Returns quantity of items in cart.

        Only used when not already iterating over the cart items.

        Return:
            int: Quantity of items in cart
        """

        return sum(
            int(item["item_quantity"])
            for item in self.cart_data["cart_items"].values()
        )
