#!/usr/bin/env python
"""URLconf for Orders app."""

from django.urls import path

from .views import OrderCreateView, OrderSuccessfulView

__author__ = "Thomas Gwasira"
__date__ = "January 2022"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


app_name = "orders"
urlpatterns = [
    path(
        "checkout/",
        OrderCreateView.as_view(),
        name="checkout",
    ),
    path(
        "order_successful/",
        OrderSuccessfulView.as_view(),
        name="order_successful",
    ),
]
