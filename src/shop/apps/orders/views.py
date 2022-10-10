#!/usr/bin/env python
"""Views for Orders app."""

# Standard library imports
import json

from itertools import chain

# Django library imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

# Third-party library imports
from moneyed.classes import Money

# Local application imports
from apps.cart.cart import Cart
from apps.contact_details.forms import (
    GuestCustomerAddressCreationInlineFormset,
    CustomerAddressCreationForm,
)
from apps.products.models.product_models import ProductVariant
from apps.users.forms import (
    GuestCustomerProfileCreationInlineFormset,
    GuestCustomerUserCreationForm,
)

from .forms import OrderCreationForm
from .models.order_models import Order, OrderLineItem, OrderShipping

from shop.constants import DEFAULT_CURRENCY


__author__ = "Thomas Gwasira"
__date__ = "January 2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class OrderCreateView(CreateView):
    """View for creation of
    :py:model:`~apps.orders.models.order_models.Order`.

    This can also be referred to as the checkout page.
    """

    login_url = reverse_lazy("users:customer_login")
    redirect_field_name = "redirect_to"
    template_name = "orders/registered_checkout.html"
    form_class = OrderCreationForm

    def get_initial(self):
        """Pre-populates initial
        :py:class:`~apps.orders.forms.OrderCreationForm` with
        appropriate values.

        Comment:
            The user type flag checks are used first because
            they perform faster than getattr(); therefore, using
            short circuit evaluation, it should check what type
            of user it is, quickly, before doing the getattr().

        Todo:
            Benchmark performance of this. Shouldn't take long at
            all. Should be equivalent to the other order.
        """
        initial_data = {}
        user = self.request.user

        # If user has a customer_profile, get initial data
        # from it
        if getattr(user, "customer_profile", None):
            initial_data["first_name"] = user.customer_profile.first_name
            initial_data["last_name"] = user.customer_profile.last_name

        return initial_data

    def get_context_data(self, **kwargs):
        """Adds additional forms to context.

        Note:
            The main form
            :py:class:`~apps.orders.forms.OrderCreationForm` has already
            been added to the context as ``form`` using the
            py:attr:`~apps.orders.views.OrderCreateView.form_class`
            attribute.

        Note:
            The default template (which is the registered customer
            checkout template) has been set using the ``template_name``
            attribute. However, if user is to be taken to the guest
            checkout page, the template is changed within this method.
        """

        context = super(OrderCreateView, self).get_context_data(**kwargs)
        user = self.request.user

        # If user has a CustomerProfile take them to registered
        # customer checkout
        if getattr(user, "customer_profile", None):
            context["is_registered_checkout"] = True

            if self.request.POST:
                context["customer_address_form"] = CustomerAddressCreationForm(
                    self.request.POST, request=self.request
                )
            else:
                context["customer_address_form"] = CustomerAddressCreationForm(
                    request=self.request,
                )

        # Otherwise take them to guest checkout
        else:
            self.template_name = "orders/guest_checkout.html"
            context["is_registered_checkout"] = False

            if self.request.POST:
                context[
                    "guest_customer_user_form"
                ] = GuestCustomerUserCreationForm(self.request.POST)
                context[
                    "guest_customer_profile_inline_formset"
                ] = GuestCustomerProfileCreationInlineFormset(
                    self.request.POST
                )
                context[
                    "guest_customer_address_inline_formset"
                ] = GuestCustomerAddressCreationInlineFormset(
                    self.request.POST
                )

            else:
                context[
                    "guest_customer_user_form"
                ] = GuestCustomerUserCreationForm()
                context[
                    "guest_customer_profile_inline_formset"
                ] = GuestCustomerProfileCreationInlineFormset()
                context[
                    "guest_customer_address_inline_formset"
                ] = GuestCustomerAddressCreationInlineFormset()

        return context

    def create_order(
        self,
        form,
        email,
        address_line1,
        address_line2,
        town_city,
        country,
        postal_code,
        is_registered_checkout,
    ):
        """Creates
        :py:model:`~apps.orders.models.order_models.Order` and all
        related models.
        """
        cart = Cart(self.request)

        if cart.cart_data and cart.cart_data["cart_items"]:
            # Create Order
            order = Order.objects.create(
                order_no=generate_order_no(),
                email=email,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                is_registered_checkout=is_registered_checkout,
            )

            # Create OrderLineItems
            for product_variant_id_str in cart.cart_data["cart_items"]:
                product_variant = get_object_or_404(
                    ProductVariant, id=int(product_variant_id_str)
                )

                item_quantity = int(
                    cart.cart_data["cart_items"][product_variant_id_str][
                        "item_quantity"
                    ]
                )

                # Create comma separated string to represent list of OptionValues
                option_values_str = ""
                option_values = product_variant.option_values.all()
                for option_value in option_values:
                    option_values_str += f"{option_value.name},"
                option_values_str = option_values_str[:-1]

                OrderLineItem.objects.create(
                    order=order,
                    product_pk=product_variant.product.pk,
                    product_name=product_variant.product.name,
                    product_variant_pk=product_variant.pk,
                    option_values=option_values_str,
                    selling_price=product_variant.selling_price,
                    discounted_price=product_variant.discounted_price,
                    percentage_discount=product_variant.percentage_discount,
                    sku_no=product_variant.sku_no,
                    order_item_quantity=item_quantity,
                    total_price=product_variant.get_price_with_multiple_items(
                        item_quantity
                    ),
                )

            # Create OrderShipping for shipping details
            # Setup shipping details
            shipping_method = form.cleaned_data.get("shipping_method")
            shipping_method_pk = ""
            shipping_method_name = ""
            shipping_method_approx_speed = ""
            shipping_method_approx_cost = ""
            if shipping_method:
                shipping_method_pk = shipping_method.pk
                shipping_method_name = shipping_method.name
                shipping_method_approx_speed = shipping_method.approx_speed
                shipping_method_approx_cost = shipping_method.approx_cost

            OrderShipping.objects.create(
                order=order,
                speed=shipping_method_approx_speed,
                cost=shipping_method_approx_cost,
                # Shipping method details
                shipping_method_pk=shipping_method_pk,
                shipping_method_name=shipping_method_name,
                # Shipping address details
                address_line1=address_line1,
                address_line2=address_line2,
                town_city=town_city,
                country=country,
                postal_code=postal_code,
            )

            # TODO: Clear cart after placing order

            return redirect(reverse_lazy("orders:order_successful"))
        # TODO: Send system message saying user tried to create an order without
        # cart items
        return render(self.request, "shop/404.html", {})

    def form_invalid(self, request, form):
        """If the form is invalid, render the invalid form."""
        return render(
            self.request, self.template_name, self.get_context_data(form=form)
        )

    def form_valid(self, form):
        context = self.get_context_data()

        # --------------------------------------------
        # Registered Customer Checkout Form Processing
        # --------------------------------------------
        if context["is_registered_checkout"] == True:
            customer_address_form = context["customer_address_form"]
            if form.is_valid() and customer_address_form.is_valid():
                registered_customer_user = self.request.user
                # TODO: Allow customer to select from existing addresses
                customer_address = customer_address_form.save()

                # Create Order and all other related models
                return self.create_order(
                    self=self,
                    form=form,
                    email=registered_customer_user.email,
                    address_line1=customer_address.address_line1,
                    address_line2=customer_address.address_line2,
                    town_city=customer_address.town_city,
                    country=customer_address.country,
                    postal_code=customer_address.postal_code,
                    is_registered_checkout=True,
                )

            else:
                return self.form_invalid(self, form)

        # ---------------------------------------
        # Guest Customer Checkout Form Processing
        # ---------------------------------------
        else:
            guest_customer_user_form = context["guest_customer_user_form"]
            guest_customer_profile_inline_formset = context[
                "guest_customer_profile_inline_formset"
            ]
            guest_customer_address_inline_formset = context[
                "guest_customer_address_inline_formset"
            ]

            if (
                form.is_valid()
                and guest_customer_user_form.is_valid()
                and guest_customer_profile_inline_formset.is_valid()
                and guest_customer_address_inline_formset.is_valid()
            ):
                # Save forms (models) for guest customer
                guest_customer_user = guest_customer_user_form.save()
                guest_customer_profile_inline_formset.instance = (
                    guest_customer_user
                )
                guest_customer_profile = (
                    guest_customer_profile_inline_formset.save(commit=False)[0]
                )

                guest_customer_profile.first_name = form.cleaned_data[
                    "first_name"
                ]
                guest_customer_profile.last_name = form.cleaned_data[
                    "last_name"
                ]
                guest_customer_profile.save()

                # Saving formset above returns a list with just 1 element
                # print(guest_customer_profile)
                guest_customer_address_inline_formset.instance = (
                    guest_customer_profile
                )
                guest_customer_address = (
                    guest_customer_address_inline_formset.save()[0]
                )

                # Create Order and all other related models
                return self.create_order(
                    form=form,
                    email=guest_customer_user.email,
                    address_line1=guest_customer_address.address_line1,
                    address_line2=guest_customer_address.address_line2,
                    town_city=guest_customer_address.town_city,
                    country=guest_customer_address.country,
                    postal_code=guest_customer_address.postal_code,
                    is_registered_checkout=False,
                )

            else:
                return self.form_invalid(self, form)


class OrderSuccessfulView(TemplateView):
    template_name = "orders/order_successful.html"
