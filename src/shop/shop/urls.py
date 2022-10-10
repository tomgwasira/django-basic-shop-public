#!/usr/bin/env python
"""Project's main URL Configuration. """

# Django library imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Local application imports
from apps.products.views import ProductListingAllView

from shop import settings

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


urlpatterns = [
    path("", ProductListingAllView.as_view(), name="index"),
    path("api/", include("api.urls")),
    path("cart/", include("apps.cart.urls")),
    path("orders/", include("apps.orders.urls")),
    path("products/", include("apps.products.urls")),
    path("search/", include("apps.search.urls")),
    path("users/", include("apps.users.urls")),
    path("nested_admin/", include("nested_admin.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
