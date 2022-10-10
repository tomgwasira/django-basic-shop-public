#!/usr/bin/env python
"""Tests for models defined in
:py:mod:`~apps.products.models.image_models`.
"""

# Django library imports
from django.db.models.fields.files import ImageFieldFile
from django.urls import reverse

# Third party library imports
import pytest

# Local application imports
from apps.products.models.note_models import *
from apps.products.models.product_models import *

from tests.factories.products.image_models_factories import *
from tests.mixins import ValidationErrorTestMixin


# =============================
# CategoryHeroImage Model Tests
# =============================
@pytest.mark.django_db
class TestCategoryHeroImageModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.CategoryHeroImage`.
    """

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.category_hero_models.CategoryHeroImage` object
        """
        CategoryHeroImageFactory()

    # -----------
    # Field Tests
    # -----------
    def test_category_hero_image_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.category_hero_models.CategoryHeroImage`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        category_hero_image = CategoryHeroImage.objects.get(id=1)

        assert len(category_hero_image._meta.get_fields()) == 5
        assert isinstance(category_hero_image.image, ImageFieldFile)
        assert isinstance(category_hero_image.category, Category)
        assert isinstance(category_hero_image.index, int)

    def test_image_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.CategoryHeroImage.image`
        has the appropriate field attribute values.
        """
        category_hero_image = CategoryHeroImage.objects.get(id=1)

        assert (
            category_hero_image._meta.get_field("image").upload_to
            == "apps/products/static/products/img/categories"
        )

    def test_category_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.CategoryHeroImage.category`
        has the appropriate field attribute values.
        """
        category_hero_image = CategoryHeroImage.objects.get(id=1)

        assert (
            getattr(
                category_hero_image._meta.get_field("category").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_index_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.CategoryHeroImage.index`
        has the appropriate field attribute values.
        """
        # Nothing to test
        pass

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.category_hero_models.CategoryHeroImage` objects
        are ordered by appropriate attribute(s)."""

        category_hero_image = CategoryHeroImage.objects.get(id=1)

        assert (
            category_hero_image._meta.order_with_respect_to.name == "category"
        )

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.category_hero_models.CategoryHeroImage` model
        is as expected.
        """

        category_hero_image = CategoryHeroImage.objects.get(id=1)

        assert category_hero_image._meta.verbose_name == "Category Hero Image"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.category_hero_models.CategoryHeroImage` model
        is as expected.
        """

        category_hero_image = CategoryHeroImage.objects.get(id=1)

        assert (
            category_hero_image._meta.verbose_name_plural
            == "Category Hero Images"
        )

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.category_hero_models.CategoryHeroImage`
        object is as expected.
        """
        category_hero_image = CategoryHeroImage.objects.get(id=1)

        assert str(category_hero_image) == f"{category_hero_image.image}"

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.category_hero_models.CategoryHeroImage`
        object is as expected.
        """
        category_hero_image = CategoryHeroImage.objects.get(id=1)

        expected_repr = {
            "image": category_hero_image.image,
            "category": category_hero_image.category._as_dict(),
            "index": category_hero_image.index,
        }

        assert category_hero_image._as_dict() == expected_repr


# ========================
# ProductImage Model Tests
# ========================
@pytest.mark.django_db
class TestProductImageModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.ProductImage`.
    """

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.ProductImage` object
        """
        ProductImageFactory()

    # -----------
    # Field Tests
    # -----------
    def test_product_image_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.ProductImage`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        product_image = ProductImage.objects.get(id=1)

        assert len(product_image._meta.get_fields()) == 5
        assert isinstance(product_image.image, ImageFieldFile)
        assert isinstance(product_image.product, Product)
        assert isinstance(product_image.index, int)

    def test_image_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductImage.image`
        has the appropriate field attribute values.
        """
        product_image = ProductImage.objects.get(id=1)

        assert (
            product_image._meta.get_field("image").upload_to
            == "apps/products/static/products/img/products"
        )

    def test_product_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductImage.product`
        has the appropriate field attribute values.
        """
        product_image = ProductImage.objects.get(id=1)

        assert (
            getattr(
                product_image._meta.get_field("product").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_index_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductImage.index`
        has the appropriate field attribute values.
        """
        # Nothing to test
        pass

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.ProductImage` objects
        are ordered by appropriate attribute(s)."""

        product_image = ProductImage.objects.get(id=1)

        assert product_image._meta.order_with_respect_to.name == "product"

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_models.ProductImage` model
        is as expected.
        """

        product_image = ProductImage.objects.get(id=1)

        assert product_image._meta.verbose_name == "Product Image"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_models.ProductImage` model
        is as expected.
        """

        product_image = ProductImage.objects.get(id=1)

        assert product_image._meta.verbose_name_plural == "Product Images"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_models.ProductImage`
        object is as expected.
        """
        product_image = ProductImage.objects.get(id=1)

        assert str(product_image) == f"{product_image.image}"

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_models.ProductImage`
        object is as expected.
        """
        product_image = ProductImage.objects.get(id=1)

        expected_repr = {
            "image": product_image.image,
            "product": product_image.product._as_dict(),
            "index": product_image.index,
        }

        assert product_image._as_dict() == expected_repr


# ===============================
# ProductVariantImage Model Tests
# ===============================
@pytest.mark.django_db
class TestProductVariantImageModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.ProductVariantImage`.
    """

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_variant_models.ProductVariantImage` object
        """
        ProductVariantImageFactory()

    # -----------
    # Field Tests
    # -----------
    def test_product_variant_image_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_variant_models.ProductVariantImage`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        product_variant_image = ProductVariantImage.objects.get(id=1)

        assert len(product_variant_image._meta.get_fields()) == 5
        assert isinstance(product_variant_image.image, ImageFieldFile)
        assert isinstance(
            product_variant_image.product_variant, ProductVariant
        )
        assert isinstance(product_variant_image.index, int)

    def test_image_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductVariantImage.image`
        has the appropriate field attribute values.
        """
        product_variant_image = ProductVariantImage.objects.get(id=1)

        assert (
            product_variant_image._meta.get_field("image").upload_to
            == "apps/products/static/products/img/product_variants"
        )

    def test_product_variant_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductVariantImage.product_variant`
        has the appropriate field attribute values.
        """
        product_variant_image = ProductVariantImage.objects.get(id=1)

        assert (
            getattr(
                product_variant_image._meta.get_field(
                    "product_variant"
                ).remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_index_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductVariantImage.index`
        has the appropriate field attribute values.
        """
        # Nothing to test
        pass

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_variant_models.ProductVariantImage` objects
        are ordered by appropriate attribute(s)."""

        product_variant_image = ProductVariantImage.objects.get(id=1)

        assert (
            product_variant_image._meta.order_with_respect_to.name
            == "product_variant"
        )

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_variant_models.ProductVariantImage` model
        is as expected.
        """

        product_variant_image = ProductVariantImage.objects.get(id=1)

        assert (
            product_variant_image._meta.verbose_name == "Product Variant Image"
        )

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_variant_models.ProductVariantImage` model
        is as expected.
        """

        product_variant_image = ProductVariantImage.objects.get(id=1)

        assert (
            product_variant_image._meta.verbose_name_plural
            == "Product Variant Images"
        )

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_variant_models.ProductVariantImage`
        object is as expected.
        """
        product_variant_image = ProductVariantImage.objects.get(id=1)

        assert str(product_variant_image) == f"{product_variant_image.image}"

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_variant_models.ProductVariantImage`
        object is as expected.
        """
        product_variant_image = ProductVariantImage.objects.get(id=1)

        expected_repr = {
            "image": product_variant_image.image,
            "product_variant": product_variant_image.product_variant._as_dict(),
            "index": product_variant_image.index,
        }

        assert product_variant_image._as_dict() == expected_repr
