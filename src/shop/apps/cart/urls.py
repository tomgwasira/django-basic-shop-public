#!/usr/bin/env python
"""URLconf for cart app."""

from django.urls import path

from . import views

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


app_name = "cart"
urlpatterns = [
    path("", views.CartSummaryView.as_view(), name="cart_summary"),
    path("cart_action/", views.CartActionView.as_view(), name="cart_action"),
]
