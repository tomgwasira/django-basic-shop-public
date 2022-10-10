#!/usr/bin/env python
"""API views for Users app."""

# Django REST Framework Library
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import (
    generics,
    views,
    mixins,
    viewsets,
    exceptions,
    response,
    permissions,
    status,
)

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
from ..serializers.users import (
    AuthUserSerializer,
    CustomerAccountSerializer,
)


__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class AuthUserView(views.APIView):
    """View for basic (non-sensitive) information about authenticated user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = AuthUserSerializer(user)

            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        except Exception:
            return response.Response(
                {
                    "error": "Something went wrong while trying to retrieve"
                    + "user details"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomerSignupView(generics.CreateAPIView):
    """View for customer sign up."""

    serializer_class = CustomerAccountSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except exceptions.ValidationError as e:
            # print(e.args)
            return response.Response(
                e.detail, status=status.HTTP_400_BAD_REQUEST
            )

    # def create(self, request, *args, **kwargs):
    #     # Create user and profile and return user data
    #     try:
    #         res = super().create(request, *args, **kwargs)
    #         return response.Response(
    #             res.data,
    #             status=status.HTTP_200_OK,
    #         )
    #     except exceptions.ValidationError as e:
    #         print(e)
    #         return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class CustomerAccountView(generics.RetrieveUpdateAPIView):
    """View for customer account management."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = CustomerAccountSerializer(user)

            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        except Exception:
            return response.Response(
                {
                    "error": "Something went wrong while trying to retrieve account details."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
