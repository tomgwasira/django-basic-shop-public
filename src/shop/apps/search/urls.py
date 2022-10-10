#!/usr/bin/env python
"""URLconf for products app."""

from django.urls import path

from . import views

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


app_name = 'search'
urlpatterns = [
    path('products/', views.ProductSearchView.as_view(), name='product_search_result'),
]
