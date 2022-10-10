"""Serializers for management of models defined in the *Products* app on the 
admin site."""

# Django REST Framework library
from rest_framework import serializers

# Third-party libraries
from api.serializers.base_serializers import (
    PrimaryKeyRelatedFieldWithDetailedRepresentation,
)
from api.serializers.products import (
    ProductImageSerializer,
    ProductThumbnailImageSerializer,
)
from djmoney.money import Money

# Django REST Framework Library
from drf_writable_nested import UniqueFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer

# Local application library
from apps.products.mixins.admin_mixins import (
    ProductAdminMixin,
    ProductVariantAdminMixin,
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
)

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class CategoryAdminSerializer(serializers.ModelSerializer):
    """Serializer for
    :py:model:`~apps.products.models.product_models.Category` objects for use
    on admin site.
    """

    class Meta:
        model = Category
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class OptionValueAdminSerializer(serializers.ModelSerializer):
    """See Product docstring and naming."""

    class Meta:
        model = OptionValue
        fields = (
            "pk",
            "name",
            "unit",
            # "display_symbol",
            "sku_symbol",
        )

    # TODO: Prevent 2 validations


class OptionTypeAdminSerializer(
    UniqueFieldsMixin, WritableNestedModelSerializer
):
    """See Product docstring and naming."""

    option_values = OptionValueAdminSerializer(many=True)

    class Meta:
        model = OptionType
        fields = (
            "pk",
            "name",
            "display_name",
            "position",
            "description",
            "option_values",
        )


class OptionTypeListAdminSerializer(serializers.ModelSerializer):
    """See Product docstring and naming."""

    option_values = OptionValueAdminSerializer(many=True)

    class Meta:
        model = OptionType
        fields = ("pk", "name", "display_name", "slug", "option_values")


class BrandAdminSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    """See Product docstring and naming."""

    class Meta:
        model = Brand
        fields = ("pk", "name", "slug", "position")


class BrandListAdminSerializer(serializers.ModelSerializer):
    """See Product docstring and naming."""

    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
            "slug",
            "position",
        )


class SupplierAdminSerializer(
    UniqueFieldsMixin, WritableNestedModelSerializer
):
    """See Product docstring and naming."""

    class Meta:
        model = Supplier
        fields = (
            "pk",
            "name",
            "details",
        )


class SupplierListAdminSerializer(serializers.ModelSerializer):
    """See Product docstring and naming."""

    class Meta:
        model = Supplier
        fields = (
            "pk",
            "id",
            "name",
        )


class ProductVariantDetailAdminSerializer(
    ProductVariantAdminMixin, serializers.ModelSerializer
):
    """Serializer for details of single
    :py:model:`~apps.products.models.product_models.ProductVariant` object for
    use on admin site.
    """

    option_values = PrimaryKeyRelatedFieldWithDetailedRepresentation(
        many=True, allow_null=True, queryset=OptionValue.objects.all()
    )

    class Meta:
        model = ProductVariant
        fields = (
            "pk",
            "option_values",
            "stock",
            "selling_price",
            "discounted_price",
        )

    def validate_option_values(self, data):
        # TODO: Fix all parts where you do indexing instead of get
        if self.parent:
            (
                is_valid,
                error_messages,
            ) = self._validate_option_type_option_value_pairings(
                data, self.parent.parent.initial_data["option_types"]
            )

            if not is_valid:
                raise serializers.ValidationError(error_messages)

        return data

    def create(self, validated_data):
        # Generate sku_no and add it to validated data
        sku_no = self.generate_sku_no(validated_data)
        validated_data["sku_no"] = sku_no

        return super(ProductVariantDetailAdminSerializer, self).create(
            validated_data
        )

    def update(self, instance, validated_data):
        # Generate sku_no and add it to validated data
        sku_no = self.generate_sku_no(validated_data)
        validated_data["sku_no"] = sku_no

        return super(ProductVariantDetailAdminSerializer, self).update(
            instance, validated_data
        )


class ProductDetailAdminSerializer(
    UniqueFieldsMixin, ProductAdminMixin, WritableNestedModelSerializer
):
    """Serializer for details of single
    :py:model:`~apps.products.models.product_models.Product` object for
    use on admin site.

    Why did we not use WritableNested again? When you override create and update to
    allow adding m2m fields using set, you have to completely define the create and update and can’t use drf-writable-nested.

    TODO: Remove UniqueFieldsMixin?
    """

    categories = PrimaryKeyRelatedFieldWithDetailedRepresentation(
        many=True, allow_null=True, queryset=Category.objects.all()
    )
    option_types = PrimaryKeyRelatedFieldWithDetailedRepresentation(
        many=True, allow_null=True, queryset=OptionType.objects.all()
    )
    brands = PrimaryKeyRelatedFieldWithDetailedRepresentation(
        many=True, allow_null=True, queryset=Brand.objects.all()
    )
    product_variants = ProductVariantDetailAdminSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "subtitle",
            "sku_symbol",
            "categories",
            "brands",
            "description",
            "option_types",
            "product_variants",
        )

    def validate_categories(self, data):
        is_valid, error_messages = self._validate_category_branches(data)

        if not is_valid:
            raise serializers.ValidationError(error_messages)

        return data

    def validate(self, data):
        is_valid, error_messages = self._validate_product_and_populate_fields(
            data
        )

        if not is_valid:
            raise serializers.ValidationError(error_messages)

        return data


class ProductListAdminSerializer(serializers.ModelSerializer):
    """Serializer for list of
    :py:model:`~apps.products.models.product_models.Product` objects on admin
    site.
    """

    categories = PrimaryKeyRelatedFieldWithDetailedRepresentation(
        many=True, allow_null=True, queryset=Category.objects.all()
    )
    product_thumbnail_images = ProductThumbnailImageSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "pk",
            "slug",
            "name",
            "categories",
            "status",
            "product_thumbnail_images",
        )
