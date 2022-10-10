#!/usr/bin/env python
"""Models related to orders in the Orders app."""

# Django library imports
from django.db import models
from django.db.models import CharField, Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import (
    BooleanField,
    DateTimeField,
    DecimalField,
    EmailField,
    PositiveIntegerField,
    TextField,
)
from django.db.models.fields.related import ForeignKey, OneToOneField

# Third-party library imports
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator

# Local application imports
from shop.constants import (
    CURRENCY_DP,
    DEFAULT_CURRENCY,
    MIN_COST,
    MAX_SKU_LENGTH,
    PERCENTAGE_DISCOUNT_DP,
)


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class Order(Model):
    """Order made by customer.

    Foreign keys are not used for models that can be changed or deleted
    in the future as this would result in the order being changed as
    well. Instead, data is extracted from the models and stored as
    attributes of this model. An alternative would have been to
    serialize the model; however, this would be less performant. Any
    extra data can be found by looking in the history tables.
    """

    order_no = CharField(max_length=10, unique=True)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    email = EmailField(blank=True, null=True)
    is_registered_checkout = BooleanField(default=False)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Totals
    # base_total
    # profit
    # net_total

    class Meta:
        ordering = ("updated_at",)
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.order_no


class OrderLineItem(Model):
    """Order line item.

    Foreign keys are not used for models that can be changed or deleted
    in the future as this would result in the order being changed as
    well. Instead, data is extracted from the models and stored as
    attributes of this model. An alternative would have been to
    serialize the model; however, this would be less performant. Any
    extra data can be found by looking in the history tables.
    """

    order = ForeignKey(Order, on_delete=CASCADE)

    # Product data
    product_pk = CharField(max_length=1000000)
    product_name = CharField(max_length=100)

    # ProductVariant data
    product_variant_pk = CharField(max_length=1000000)
    option_values = CharField(max_length=10000, blank=True, null=True)

    selling_price = MoneyField(
        max_digits=19,
        decimal_places=CURRENCY_DP,
        default_currency=DEFAULT_CURRENCY,
    )
    discounted_price = MoneyField(
        max_digits=19,
        decimal_places=CURRENCY_DP,
        default_currency=DEFAULT_CURRENCY,
        null=True,
        blank=True,
    )
    percentage_discount = DecimalField(
        max_digits=4,
        decimal_places=PERCENTAGE_DISCOUNT_DP,
        null=True,
        blank=True,
    )
    sku_no = CharField(max_length=MAX_SKU_LENGTH)

    order_item_quantity = PositiveIntegerField()
    total_price = MoneyField(
        max_digits=19,
        decimal_places=CURRENCY_DP,
        default_currency=DEFAULT_CURRENCY,
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = "order"
        verbose_name = "Order Line Item"
        verbose_name_plural = "Order Line Items"

    def __str__(self):
        """Returns
        :py:attr:`~apps.orders.models.order_models.Order.order_no`
        and
        :py:attr:`~apps.orders.models.order_models.OrderLineItem.id`
        as string representation of the
        :py:model:`~apps.orders.models.order_models.OrderLineItem`.

        Returns:
            str: String representation of the
                :py:model:`~apps.orders.models.order_models.OrderLineItem`.
        """
        return f"Order No. {self.order.order_no}: Item {self.id}"


class OrderPayment(Model):
    """Details about payment for an order."""

    # Cannot insert this relationship in Order instead
    # because will not be able to use inlines etc.
    order = OneToOneField(
        Order, on_delete=CASCADE, related_name="order_payment"
    )

    # Payment status choices
    AWAITING_PAYMENT = "awaiting_payment"
    PAID = "paid"
    CANCELLED = "cancelled"
    PAYMENT_STATUS = [
        (AWAITING_PAYMENT, "Awaiting payment"),
        (PAID, "Fully paid for"),
        (CANCELLED, "Payment cancelled"),
    ]

    status = CharField(
        max_length=32,
        choices=PAYMENT_STATUS,
        default=AWAITING_PAYMENT,
    )


class OrderShippingMethod(Model):
    """Shipping method for a particular order.

    The selection of shipping method is presented to the customer on the
    checkout page.
    """

    name = CharField(max_length=1000, unique=True)
    approx_speed = CharField(max_length=1000)
    approx_cost = MoneyField(
        max_digits=19,
        decimal_places=CURRENCY_DP,
        default_currency=DEFAULT_CURRENCY,
        validators=[MinMoneyValidator(MIN_COST)],
    )
    is_active = BooleanField(default=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Order Shipping Method"
        verbose_name_plural = "Order Shipping Methods"

    def __str__(self):
        """Returns
        :py:attr:`~apps.orders.models.order_models.ShippingMethod.name`
        as string representation of the
        :py:model:`~apps.orders.models.order_models.Shipping`.

        Returns:
            str: String representation of the
                :py:model:`~apps.orders.models.order_models.ShippingMethod`.
        """
        return self.name

    def _as_dict(self):
        """Returns dictionary representation of the
        :py:model:`~apps.orders.models.order_models.ShippingMethod`
        which includes dictionary representations of any related
        model objects.

        Returns:
            dict: Dictionary representation of the
                :py:model:`~apps.orders.models.order_models.ShippingMethod`.

        Todo:
            Implement this method.
        """
        pass


class OrderShipping(Model):
    """Details about shipping of an order.

    Todo:
        When testing, test that attributes in two models corresponding
        to each other e.g. shipping_method_name and OrderShippingMethod.name
        have same built in validators e.g. max_length.
    """

    # Cannot insert this relationship in Order instead
    # because will not be able to use inlines etc.
    order = OneToOneField(
        Order, on_delete=CASCADE, related_name="order_shipping"
    )

    address_line1 = CharField(max_length=200)
    address_line2 = CharField(max_length=200, blank=True)
    town_city = CharField(max_length=200, blank=True)
    country = CharField(max_length=200)
    postal_code = CharField(max_length=50, blank=True)

    # Shipping status choices
    AWAITING_SCHEDULING = "awaiting_scheduling"
    SCHEDULED = "scheduled"
    AWAITING_PICKUP = "awaiting_pickup"
    SHIPPED = "shipped"
    SHIPPING_STATUS = [
        (
            AWAITING_SCHEDULING,
            "Awaiting setting of shipping date and other details",
        ),
        (
            SCHEDULED,
            "A shipping date and other mandatory details have been set",
        ),
        (AWAITING_PICKUP, "Awaiting pickup"),
        (SHIPPED, "Order is out for shipping"),
    ]

    status = CharField(
        max_length=32,
        choices=SHIPPING_STATUS,
        default=AWAITING_SCHEDULING,
    )

    # consider changing this to a custom field with number and units
    # and methods for addition etc.
    shipping_method_pk = TextField()
    shipping_method_name = CharField(max_length=1000)
    speed = CharField(max_length=1000)
    cost = MoneyField(
        max_digits=19,
        decimal_places=CURRENCY_DP,
        default_currency=DEFAULT_CURRENCY,
        validators=[MinMoneyValidator(MIN_COST)],
    )
    # date scheduled
    # allow changing of shipping method
    # order_shipping_method = ForeignKey(OrderShippingMethod, on_delete=SET_NULL)
    # only change when id of shipping method changes but don't change it to null
    # order_shipping_method_json = JSONField()

    # allow changing of shipper
    # shipper = ForeignKey(Shipper, on_delete=SET_NULL)
    # shipper_json_at_creation = JSONField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class OrderDelivery(Model):
    """Details about delivery of an order."""

    # Cannot insert this relationship in Order instead
    # because will not be able to use inlines etc.
    order = OneToOneField(
        Order, on_delete=CASCADE, related_name="order_delivery"
    )

    # Delivery status choices
    AWAITING_DELIVERY = "awaiting_delivery"
    DELIVERED = "delivered"
    DELIVERY_STATUS = [
        (AWAITING_DELIVERY, "Awaiting delivery"),
        (DELIVERED, "Delivered and signed for"),
    ]

    status = CharField(
        max_length=32,
        choices=DELIVERY_STATUS,
        default=AWAITING_DELIVERY,
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
