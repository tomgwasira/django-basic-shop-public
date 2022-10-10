#!/usr/bin/env python
"""URLconf for Products app."""

from django.urls import path

from . import views

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


app_name = "products"
urlpatterns = [
    path(
        "", views.ProductListingAllView.as_view(), name="product_listing_all"
    ),
    path(
        "option-value-selection",
        views.OptionValueSelectionView.as_view(),
        name="option_value_selection",
    ),
    path(
        "<slug:slug>/",
        views.ProductListingByCategoryView.as_view(),
        name="product_listing_by_category",
    ),
    path(
        "product/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]
