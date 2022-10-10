"""Serializers for models defined in Products app."""

# Django REST Framework Library
# Django REST Framework library
from rest_framework import serializers

# Third-party libraries
from api.serializers.base_serializers import DynamicFieldsModelSerializer

# Local application library
from apps.products.mixins.product_detail_mixin import ProductDetailMixin
from apps.products.models.image_models import (
    ProductImage,
    ProductThumbnailImage,
)

# Local Application Library
from apps.products.models.product_models import (
    Category,
    OptionType,
    OptionValue,
    Product,
    ProductVariant,
)

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


# To-do: Make note: If you serialize the whole model as is, you can just name it <Model>Serializer or is AdminSerializer better?


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.product_models.Category` objects for use
    in navbar.
    """

    class Meta:
        model = Category
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.image_models.ProductImage` objects.
    """

    class Meta:
        model = ProductImage
        fields = (
            "image",
            "option_value",
            "alt_text",
            "position",
            "is_featured",
            "is_option_value_icon",
        )


class ProductThumbnailImageSerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.image_models.ProductThumbnailImage` objects.
    """

    class Meta:
        model = ProductThumbnailImage
        fields = (
            "image",
            "option_value",
            "alt_text",
            "position",
            "is_featured",
            "is_option_value_icon",
        )


class OptionTypeSerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.product_models.OptionType` objects.
    """

    class Meta:
        model = OptionType
        fields = "__all__"


class OptionValueSerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.product_models.OptionValue` objects.
    """

    option_type = OptionTypeSerializer(read_only=True)

    class Meta:
        model = OptionValue
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.product_models.ProducVariant` objects.
    """

    option_values = OptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductListingProductSerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.product_models.Product` objects
    to be used for product listing page.
    """

    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "min_price_currency",
            "min_price",
            "max_price_currency",
            "max_price",
            "min_price_original_currency",
            "min_price_original",
            "max_price_original_currency",
            "max_price_original",
            "product_images",
        )
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class ProductDetailProductSerializer(
    serializers.ModelSerializer, ProductDetailMixin
):
    """Serializer for
    :py:model:`~apps.products.models.product_models.Product` objects
    to be used for product detail page.
    """

    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "description", "product_images")

    def to_representation(self, instance):
        """Add extra information to serializer output."""
        representation = super().to_representation(instance)
        (
            representation["option_types"],
            representation["product_variants"],
        ) = self.get_product_detail_extras(instance)

        return representation
