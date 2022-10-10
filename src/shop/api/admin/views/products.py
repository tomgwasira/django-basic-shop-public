#!/usr/bin/env python
"""API views for admin of *Products* app."""

# Standard library
import json

# Django library
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Django REST Framework library
from rest_framework import (
    generics,
    parsers,
    permissions,
    response,
    status,
    viewsets,
)
from rest_framework.decorators import action

# Third-party libraries
import ujson
from attr import validate

# Local application library
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
    BrandAdminSerializer,
    BrandListAdminSerializer,
    CategoryAdminSerializer,
    OptionTypeAdminSerializer,
    OptionTypeListAdminSerializer,
    ProductDetailAdminSerializer,
    ProductListAdminSerializer,
    ProductVariantDetailAdminSerializer,
    SupplierAdminSerializer,
    SupplierListAdminSerializer,
)

__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class CategoryAdminViewSet(viewsets.ModelViewSet):
    """Viewset for categories."""

    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return response.Response(
            Category.dump_bulk(),
            status=status.HTTP_200_OK,
        )


class OptionTypeAdminViewSet(viewsets.ModelViewSet):
    """Viewset for product options."""

    queryset = OptionType.objects.filter(is_active=True)
    serializer_class = OptionTypeAdminSerializer
    lookup_field = "slug"
    # permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request):
        # Use different serializer class for list
        self.serializer_class = OptionTypeListAdminSerializer
        return super().list(self, request)


class BrandAdminViewset(viewsets.ModelViewSet):
    """Viewset for admin pages related to
    :py:model:`~apps.products.models.product_models.Brand` objects."""

    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandAdminSerializer
    lookup_field = "slug"
    # permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request):
        # Use different serializer class for list
        self.serializer_class = BrandListAdminSerializer
        return super().list(self, request)

    @action(detail=True, methods=["post"])
    def soft_delete(self, request, pk=None, slug=None):
        """Perform soft delete of the
        :py:model:`~apps.products.models.product_models.Brand` object.
        """
        brand = self.get_object()

        try:
            brand.is_active = False
            brand.save()

            return response.Response(
                {"message": "Brand deleted successfully."}
            )

        except Exception:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], queryset=Brand.objects.all())
    def soft_undelete(self, request, pk=None, slug=None):
        """Perform soft undelete of the
        :py:model:`~apps.products.models.product_models.Brand` object.
        """
        brand = self.get_object()

        try:
            brand.is_active = True
            brand.save()

            return response.Response(
                {"message": "Brand undeleted successfully."}
            )

        except Exception:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def list_soft_deleted(self, request):
        """Retrieve all soft deleted
        :py:model:`~apps.products.models.product_models.Brand` objects.
        ordered by when each object was last updated.
        """
        brands = Brand.objects.all(is_active=False).order_by("-updated_at")


class SupplierAdminViewset(viewsets.ModelViewSet):
    """Viewset for admin pages related to
    :py:model:`~apps.products.models.product_models.Supplier` objects.
    """

    queryset = Supplier.objects.filter(is_active=True)
    serializer_class = SupplierAdminSerializer
    # permission_classes = [permissions.DjangoModelPermissions]

    def list(self, request):
        # Use different serializer class for list
        self.serializer_class = SupplierListAdminSerializer

        return super().list(self, request)

    @action(detail=True, methods=["post"])
    def soft_delete(self, request, pk=None):
        """Perform soft delete of the
        :py:model:`~apps.products.models.product_models.Supplier` object.
        """
        supplier = self.get_object()

        try:
            supplier.is_active = False
            supplier.save()

            return response.Response(
                {"message": "Supplier deleted successfully."}
            )

        except Exception:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], queryset=Supplier.objects.all())
    def soft_undelete(self, request, pk=None):
        """Perform soft undelete of the
        :py:model:`~apps.products.models.product_models.Supplier` object."""
        supplier = self.get_object()

        try:
            supplier.is_active = True
            supplier.save()

            return response.Response(
                {"message": "Supplier undeleted successfully."}
            )

        except Exception:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)


class ProductAdminViewset(viewsets.ModelViewSet):
    """Viewset for admin pages to manage
    :py:model:`~apps.products.models.product_models.Product` and other related
    objects.
    """

    # TODO: Allow list actions like bulk soft_delete.

    queryset = Product.objects.all()
    serializer_class = ProductDetailAdminSerializer
    # permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = "slug"

    @action(
        detail=False,
        url_path="validate-product-variant",
        url_name="validate_product_variant",
        methods=["post"],
    )
    def validate_product_variant(self, request, pk=None):
        serializer = ProductVariantDetailAdminSerializer(data=request.data)
        if serializer.is_valid():
            return JsonResponse(
                {"data": "Product variant data valid."}, status=200
            )
        return JsonResponse(serializer.errors, status=400)

    def create(self, request, *args, **kwargs):
        serializer = ProductDetailAdminSerializer(
            data=ujson.loads(request.data.get("form_data"))
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
        # return response.Response({"received data": request.data})

    @action(
        detail=True,
        url_path="soft-delete",
        url_name="soft_delete",
        methods=["patch"],
    )
    def soft_delete(self, request, *args, **kwargs):
        # TODO: Use app variables for this
        # TODO: Use try catch
        product = self.get_object()
        product.status = 3
        product.save()

        return JsonResponse(
            {"data": "Product deleted successfully."}, status=200
        )

    def list(self, request):
        # Use different serializer class for list
        self.serializer_class = ProductListAdminSerializer
        self.queryset = Product.objects.filter(status=1)

        return super(ProductAdminViewset, self).list(request)

    @action(detail=False)
    def list_archived(self, request):
        self.serializer_class = ProductListAdminSerializer
        self.queryset = Product.objects.filter(status=2)

        return super(ProductAdminViewset, self).list(request)

    # @action(detail=False)
    # def list_deleted(self, request):
    #     self.serializer_class = ProductListAdminSerializer
    #     self.queryset = Product.objects.filter(status=3)

    #     return super(ProductAdminViewset, self).list(request)
