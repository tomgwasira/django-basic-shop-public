#!/usr/bin/env python
"""API views for Products app."""
# Standard library
import json

# Django library
# Django REST Framework Library
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Django REST Framework library
from rest_framework import generics, permissions, response, status, viewsets

# Local application library
# Local Application Library
from apps.products.models.product_models import (
    Brand,
    Category,
    OptionType,
    OptionValue,
    Product,
    ProductVariant,
    Supplier,
    Tag,
)

from ..serializers.products import (
    CategorySerializer,
    ProductDetailProductSerializer,
    ProductListingProductSerializer,
)

__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class CategoriesViewset(viewsets.ModelViewSet):
    """Viewset for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return response.Response(
            Category.dump_bulk(),
            status=status.HTTP_200_OK,
        )


class ProductsViewSet(viewsets.ModelViewSet):
    """Viewset for products."""

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListingProductSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        """Use different serializer for specific actions."""

        if self.action == "retrieve":
            return ProductDetailProductSerializer
        return self.serializer_class
