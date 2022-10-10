from django.contrib import admin
from django.contrib.admin import ModelAdmin, register, TabularInline

from apps.orders.models.order_models import (
    Order,
    OrderLineItem,
    OrderShipping,
    OrderShippingMethod,
)


class OrderLineItemInline(TabularInline):
    """Inline for
    :py:model:`~apps.products.models.note_models.SupplierNote` on
    :py:class:`~apps.products.admin.SupplierAdmin` page.
    """

    model = OrderLineItem
    extra = 0


class OrderShippingInline(TabularInline):
    """Inline for
    :py:model:`~apps.products.models.note_models.SupplierNote` on
    :py:class:`~apps.products.admin.SupplierAdmin` page.
    """

    model = OrderShipping
    extra = 0


@register(Order)
class OrderAdmin(ModelAdmin):
    inlines = (OrderLineItemInline, OrderShippingInline)


admin.site.register(OrderShippingMethod)
