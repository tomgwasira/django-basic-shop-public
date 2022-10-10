#!/usr/bin/env python
"""Tests for models defined in
:py:mod:`~apps.products.models.product_models`.
"""

# Standard library
import datetime
import uuid
from decimal import Decimal, DivisionByZero

# Django library
from django.db import models
from django.urls import reverse

# Third-party libraries
import pytest
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from model_bakery import baker

# Local application library
from apps.products.models.product_models import *
from apps.products.models.product_models import (
    Category,
    OptionType,
    OptionValue,
)
from shop import constants
from tests.mixins import ValidationErrorTestMixin

__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"

# pytest -s src/shop/tests/unit/apps/products/models/test_product_models.py

# ====================
# Category Model Tests
# ====================
@pytest.mark.django_db
class TestCategoryModel:
    """Tests for the :py:class:`~apps.products.models.product_models.Category`
    model."""

    # ------------------
    # Setup and Teardown
    # ------------------
    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        root = Category.add_root()
        category_1 = root.add_child(
            name="Test Category 1", description="Test Category 1 description."
        )
        category_2 = category_1.add_child(
            name="Test Category 2", description="Test Category 2 description."
        )
        category_3 = category_2.add_child(
            name="Test Category 3", description="Test Category 3 description."
        )
        category_2.add_child(
            name="Test Category 4", description="Test Category 4 description"
        )
        category_3.add_child(
            name="Test Category 3_1",
            description="Test Category 3_1 description",
        )

    # -----------
    # Field Tests
    # -----------
    def test_category_object_has_information_fields(self):
        category = Category.objects.get(id=2)

        assert len(category._meta.get_fields()) == 15
        assert isinstance(category.name, str)
        assert isinstance(category.description, str)
        assert isinstance(category.is_active, bool)
        assert isinstance(category.slug, str)
        assert isinstance(category.created_at, datetime.datetime)
        assert isinstance(category.updated_at, datetime.datetime)
        assert isinstance(category.uuid, uuid.UUID)

    def test_name_field_attributes(self):
        category = Category.objects.get(id=2)

        assert category._meta.get_field("name").max_length == 250

    def test_description_field_attributes(self):
        category = Category.objects.get(id=2)

        assert category._meta.get_field("description").max_length == 1000
        assert category._meta.get_field("description").blank

    def test_is_active_field_attributes(self):
        category = Category.objects.get(id=2)

        assert category._meta.get_field("is_active").default

    def test_slug_field_attributes(self):
        category = Category.objects.get(id=2)

        assert category._meta.get_field("slug")._populate_from == "name"
        assert category._meta.get_field("slug").overwrite
        assert category._meta.get_field("slug").unique

    def test_created_at_field_attributes(self):
        category = Category.objects.get(id=2)

        assert category._meta.get_field("created_at").auto_now_add

    def test_updated_at_field_attributes(self):
        category = Category.objects.get(id=2)

        assert category._meta.get_field("updated_at").auto_now

    def test_uuid_field_attributes(self):
        category = Category.objects.get(id=2)

        assert not category._meta.get_field("uuid").editable

    # ----------
    # Meta Tests
    # ----------
    def test_verbose_name(self):
        category = Category.objects.get(id=2)

        assert category._meta.verbose_name == "Category"

    def test_verbose_name_plural(self):
        category = Category.objects.get(id=2)

        assert category._meta.verbose_name_plural == "Categories"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        category = Category.objects.get(id=2)

        assert str(category) == category.name

    def test_get_absolute_url(self):
        category = Category.objects.get(id=2)

        assert (
            category.get_absolute_url() == "/products/" + category.slug + "/"
        )

    def test_get_ancestors_and_self(self):
        category_4 = Category.objects.get(id=5)

        assert category_4.get_ancestors_and_self() == [
            Category.objects.get(id=1),
            Category.objects.get(id=2),
            Category.objects.get(id=3),
            Category.objects.get(id=5),
        ]

    def test_get_descendants_and_self(self):
        category_2 = Category.objects.get(id=3)

        # print(list(category_2.get_descendants_and_self()))
        assert list(category_2.get_descendants_and_self()) == [
            Category.objects.get(id=3),
            Category.objects.get(id=4),
            Category.objects.get(id=6),
            Category.objects.get(id=5),
        ]


# ======================
# OptionType Model Tests
# ======================
@pytest.mark.django_db
class TestOptionTypeModel:
    """Tests for the OptionType model."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        baker.make(OptionType)

    # -----------
    # Field Tests
    # -----------
    def test_option_type_object_has_information_fields(self):
        option_type = OptionType.objects.get(id=1)

        assert len(option_type._meta.get_fields()) == 13
        assert isinstance(option_type.name, str)
        assert isinstance(option_type.display_name, str)
        assert isinstance(option_type.description, str)
        assert isinstance(option_type.position, Decimal)
        assert isinstance(option_type.is_active, bool)
        assert isinstance(option_type.slug, str)
        assert isinstance(option_type.created_at, datetime.datetime)
        assert isinstance(option_type.updated_at, datetime.datetime)
        assert isinstance(option_type.uuid, uuid.UUID)
        assert isinstance(
            option_type._meta.get_field("option_values"), models.ManyToOneRel
        )

    def test_name_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.get_field("name").max_length == 250
        assert option_type._meta.get_field("name").unique

    def test_display_name_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.get_field("display_name").max_length == 250
        assert option_type._meta.get_field("display_name").blank

    def test_description_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.get_field("description").max_length == 1000
        assert option_type._meta.get_field("description").blank

    def test_position_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert (
            option_type._meta.get_field("position").max_digits
            == constants.POSITION_MAX_DIGITS
        )
        assert (
            option_type._meta.get_field("position").decimal_places
            == constants.POSITION_DP
        )
        assert option_type._meta.get_field("position").default == Decimal(
            1000000.0
        )

    def test_is_active_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.get_field("is_active").default

    def test_slug_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.get_field("slug")._populate_from == "name"
        assert option_type._meta.get_field("slug").overwrite
        assert option_type._meta.get_field("slug").unique

    def test_created_at_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.get_field("created_at").auto_now_add

    def test_updated_at_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.get_field("updated_at").auto_now

    def test_uuid_field_attributes(self):
        option_type = OptionType.objects.get(id=1)

        assert not option_type._meta.get_field("uuid").editable

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.ordering == ("position",)

    def test_verbose_name(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.verbose_name == "Option"

    def test_verbose_name_plural(self):
        option_type = OptionType.objects.get(id=1)

        assert option_type._meta.verbose_name_plural == "Options"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        option_type = OptionType.objects.get(id=1)

        assert str(option_type) == option_type.name


# =======================
# OptionValue Model Tests
# =======================
@pytest.mark.django_db
class TestOptionValueModel:
    """Tests for the OptionValue model."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        baker.make(OptionValue)

    # -----------
    # Field Tests
    # -----------
    def test_option_value_object_has_information_fields(self):
        option_value = OptionValue.objects.get(id=1)

        assert len(option_value._meta.get_fields()) == 13
        assert isinstance(option_value.name, str)
        assert isinstance(option_value.unit, str)
        assert isinstance(option_value.display_name, str)
        assert isinstance(option_value.option_type, OptionType)
        assert isinstance(option_value.sku_symbol, str)
        assert isinstance(option_value.is_active, bool)
        assert isinstance(option_value.created_at, datetime.datetime)
        assert isinstance(option_value.updated_at, datetime.datetime)
        assert isinstance(option_value.uuid, uuid.UUID)

    def test_name_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("name").max_length == 250
        assert (
            option_value._meta.get_field("name").verbose_name == "Name/ Value"
        )

    def test_display_name_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("display_name").max_length == 250
        assert option_value._meta.get_field("display_name").blank

    def test_unit_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("unit").max_length == 10
        assert option_value._meta.get_field("unit").blank

    def test_option_type_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert (
            getattr(
                option_value._meta.get_field("option_type").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_sku_symbol_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("sku_symbol").max_length == 5
        assert option_value._meta.get_field("sku_symbol")

    def test_is_active_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("is_active").default

    def test_created_at_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("created_at").auto_now_add

    def test_updated_at_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("updated_at").auto_now

    def test_uuid_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert not option_value._meta.get_field("uuid").editable

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.order_with_respect_to.name == "option_type"

    def test_verbose_name(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.verbose_name == "Option Value"

    def test_verbose_name_plural(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.verbose_name_plural == "Option Values"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        option_value = OptionValue.objects.get(id=1)

        assert (
            str(option_value)
            == f"{option_value.name} {option_value.unit}".strip()
        )


# # =================
# # Brand Model Tests
# # =================
# @pytest.mark.django_db
# class TestBrandModel:
#     """Tests for the Brand model."""

#     @pytest.fixture(autouse=True)
#     def setup_test_db(self, db):
#         """Sets up test database containing a basic
#         :py:model:`~apps.products.models.product_models.Brand` object
#         """
#         BrandFactory()

#     # -----------
#     # Field Tests
#     # -----------
#     def test_brand_object_has_information_fields(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Brand`
#         objects have correct number of fields and are populated
#         with values of the expected datatypes.
#         """
#         brand = Brand.objects.get(id=1)

#         assert len(brand._meta.get_fields()) == 7
#         assert isinstance(brand.name, str)
#         assert isinstance(brand.index, int)
#         assert isinstance(brand.created, datetime.datetime)
#         assert isinstance(brand.updated, datetime.datetime)

#     def test_name_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Brand.name`
#         has the appropriate field attribute values.
#         """
#         brand = Brand.objects.get(id=1)

#         assert brand._meta.get_field("name").max_length == 100
#         assert brand._meta.get_field("name").unique

#     def test_index_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Brand.index`
#         has the appropriate field attribute values.
#         """
#         brand = Brand.objects.get(id=1)

#         assert brand._meta.get_field("index").default == 1000000

#     def test_created_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Brand.created`
#         has the appropriate field attribute values.
#         """
#         brand = Brand.objects.get(id=1)

#         assert brand._meta.get_field("created").auto_now_add

#     def test_updated_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Brand.updated`
#         has the appropriate field attribute values.
#         """
#         brand = Brand.objects.get(id=1)

#         assert brand._meta.get_field("updated").auto_now

#     # ----------
#     # Meta Tests
#     # ----------
#     def test_ordering(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Brand` objects
#         are ordered by appropriate attribute(s)."""

#         brand = Brand.objects.get(id=1)

#         assert brand._meta.ordering == ("index",)

#     def test_verbose_name(self):
#         """Tests that the ``verbose_name`` of the
#         :py:model:`~apps.products.models.product_models.Brand` model
#         is as expected.
#         """

#         brand = Brand.objects.get(id=1)

#         assert brand._meta.verbose_name == "Brand"

#     def test_verbose_name_plural(self):
#         """Tests that the ``verbose_name_plural`` of the
#         :py:model:`~apps.products.models.product_models.Brand` model
#         is as expected.
#         """

#         brand = Brand.objects.get(id=1)

#         assert brand._meta.verbose_name_plural == "Brands"

#     # -------------------
#     # Custom Method Tests
#     # -------------------
#     def test_str(self):
#         """Tests that the string representation of
#         :py:model:`~apps.products.models.product_models.Brand`
#         object is as expected.
#         """
#         brand = Brand.objects.get(id=1)

#         assert str(brand) == f"{brand.name}"

#     def test_as_dict(self):
#         """Tests that the dictionary representation of
#         :py:model:`~apps.products.models.product_models.Brand`
#         object is as expected.
#         """
#         brand = Brand.objects.get(id=1)

#         expected_repr = {
#             "name": brand.name,
#             "index": brand.index,
#             "created": str(brand.created),
#             "updated": str(brand.updated),
#         }

#         assert brand._as_dict() == expected_repr


# # ====================
# # Supplier Model Tests
# # ====================
# @pytest.mark.django_db
# class TestSupplierModel:
#     """Tests for the Supplier model."""

#     @pytest.fixture(autouse=True)
#     def setup_test_db(self, db):
#         """Sets up test database containing a basic
#         :py:model:`~apps.products.models.product_models.Supplier` object
#         """
#         SupplierFactory()

#     # -----------
#     # Field Tests
#     # -----------
#     def test_supplier_object_has_information_fields(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Supplier`
#         objects have correct number of fields and are populated
#         with values of the expected datatypes.
#         """
#         supplier = Supplier.objects.get(id=1)

#         assert len(supplier._meta.get_fields()) == 7
#         assert isinstance(supplier.name, str)
#         assert isinstance(supplier.details, str)
#         assert isinstance(supplier.created, datetime.datetime)
#         assert isinstance(supplier.updated, datetime.datetime)

#     def test_name_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Supplier.name`
#         has the appropriate field attribute values.
#         """
#         supplier = Supplier.objects.get(id=1)

#         assert supplier._meta.get_field("name").max_length == 100

#     def test_details_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Supplier.details`
#         has the appropriate field attribute values.
#         """
#         supplier = Supplier.objects.get(id=1)

#         assert supplier._meta.get_field("details").max_length == 1000
#         assert supplier._meta.get_field("details").blank

#     def test_created_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Supplier.created`
#         has the appropriate field attribute values.
#         """
#         supplier = Supplier.objects.get(id=1)

#         assert supplier._meta.get_field("created").auto_now_add

#     def test_updated_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Supplier.updated`
#         has the appropriate field attribute values.
#         """
#         supplier = Supplier.objects.get(id=1)

#         assert supplier._meta.get_field("updated").auto_now

#     # ----------
#     # Meta Tests
#     # ----------
#     def test_ordering(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Supplier` objects
#         are ordered by appropriate attribute(s)."""

#         supplier = Supplier.objects.get(id=1)

#         assert supplier._meta.ordering == ("name",)

#     def test_verbose_name(self):
#         """Tests that the ``verbose_name`` of the
#         :py:model:`~apps.products.models.product_models.Supplier` model
#         is as expected.
#         """

#         supplier = Supplier.objects.get(id=1)

#         assert supplier._meta.verbose_name == "Supplier"

#     def test_verbose_name_plural(self):
#         """Tests that the ``verbose_name_plural`` of the
#         :py:model:`~apps.products.models.product_models.Supplier` model
#         is as expected.
#         """

#         supplier = Supplier.objects.get(id=1)

#         assert supplier._meta.verbose_name_plural == "Suppliers"

#     # -------------------
#     # Custom Method Tests
#     # -------------------
#     def test_str(self):
#         """Tests that the string representation of
#         :py:model:`~apps.products.models.product_models.Supplier`
#         object is as expected.
#         """
#         supplier = Supplier.objects.get(id=1)

#         assert str(supplier) == f"{supplier.name}"

#     def test_as_dict(self):
#         """Tests that the dictionary representation of
#         :py:model:`~apps.products.models.product_models.Supplier`
#         object is as expected.
#         """
#         supplier = Supplier.objects.get(id=1)

#         expected_repr = {
#             "name": supplier.name,
#             "details": supplier.details,
#             "created": str(supplier.created),
#             "updated": str(supplier.updated),
#         }

#         assert supplier._as_dict() == expected_repr


# # ====================
# # Product Model Tests
# # ====================
# @pytest.mark.django_db
# class TestProductModel(ValidationErrorTestMixin):
#     """Tests for the Product model."""

#     @pytest.fixture(autouse=True)
#     def setup_test_db(self, db):
#         """Sets up test database containing a basic
#         :py:model:`~apps.products.models.product_models.Product` object
#         """
#         ProductFactory()

#     # -----------
#     # Field Tests
#     # -----------
#     def test_product_object_has_information_fields(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Product`
#         objects have correct number of fields and are populated
#         with values of the expected datatypes.
#         """

#         product = Product.objects.get(id=1)

#         assert len(product._meta.get_fields()) == 24
#         assert isinstance(product.name, str)
#         assert isinstance(product.slug, str)
#         assert isinstance(product.sku_symbol, str)
#         assert product.categories.model == Category
#         assert product.brands.model == Brand
#         assert isinstance(product.description, str)
#         assert product.option_types.model == OptionType
#         assert isinstance(product.is_flagged, bool)
#         assert isinstance(product.created, datetime.datetime)
#         assert isinstance(product.updated, datetime.datetime)
#         assert isinstance(product.min_price, Money)
#         assert isinstance(product.max_price, Money)
#         assert isinstance(product.min_price_original, Money)
#         assert isinstance(product.max_price_original, Money)
#         assert isinstance(product.is_form_validated, bool)

#     def test_name_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.name`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("name").max_length == 100
#         assert product._meta.get_field("name").unique

#     def test_slug_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.slug`
#         has the appropriate field attribute values.

#         Note:
#             *   The slugify_function attribute is tested implicitly in
#                 :py:meth:`~tests.unit.apps.products.models.test_product_models.TestProduct.test_get_absolute_url`.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("slug")._populate_from == "name"
#         assert product._meta.get_field("slug").unique

#     def test_sku_symbol_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.sku_symbol`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("sku_symbol").max_length == 5
#         assert product._meta.get_field("sku_symbol").unique

#     def test_categories_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.categories`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert not product._meta.get_field("categories").blank
#         assert (
#             product._meta.get_field("categories").related_query_name()
#             == "products"
#         )

#     def test_brands_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.brands`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("brands").blank

#     def test_description_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.description`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("description").max_length == 1000
#         assert product._meta.get_field("description").blank

#     def test_option_types_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.option_types`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("option_types").blank

#     def test_is_flagged_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.is_flagged`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert not product._meta.get_field("is_flagged").default

#     def test_created_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.created`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("created").auto_now_add

#     def test_updated_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.updated`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("updated").auto_now

#     def test_min_price_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.min_price`
#         has the appropriate field attribute values.

#         Comment:
#             *   Validators for ``MoneyField``, albeit likely tested by the
#                 authors of the package are also tested separately within
#                 the current test class.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("min_price").max_digits == 19
#         assert (
#             product._meta.get_field("min_price").decimal_places == CURRENCY_DP
#         )
#         assert (
#             product._meta.get_field("min_price").default_currency
#             == DEFAULT_CURRENCY
#         )

#     def test_max_price_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.max_price`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("max_price").max_digits == 19
#         assert (
#             product._meta.get_field("max_price").decimal_places == CURRENCY_DP
#         )
#         assert (
#             product._meta.get_field("max_price").default_currency
#             == DEFAULT_CURRENCY
#         )

#     def test_min_price_original_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.min_price_original`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("min_price_original").max_digits == 19
#         assert (
#             product._meta.get_field("min_price_original").decimal_places
#             == CURRENCY_DP
#         )
#         assert (
#             product._meta.get_field("min_price_original").default_currency
#             == DEFAULT_CURRENCY
#         )

#     def test_max_price_original_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.max_price_original`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.get_field("max_price_original").max_digits == 19
#         assert (
#             product._meta.get_field("max_price_original").decimal_places
#             == CURRENCY_DP
#         )
#         assert (
#             product._meta.get_field("max_price_original").default_currency
#             == DEFAULT_CURRENCY
#         )

#     def test_is_form_validated_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.is_form_validated`
#         has the appropriate field attribute values.
#         """
#         product = Product.objects.get(id=1)

#         assert not product._meta.get_field("is_form_validated").default

#     # ----------------------
#     # M2m Relationship Tests
#     # ----------------------
#     def test_categories_m2m(self):
#         """Tests the m2m relationship for
#         :py:attr:`~apps.products.models.product_models.Product.categories`.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         Product.objects.get(id=1).delete()

#         root = Category.add_root()

#         category_1 = root.add_child(
#             name="Test Category 1", description="Test Category description."
#         )
#         category_2 = root.add_child(
#             name="Test Category 2", description="Test Category description."
#         )
#         category_3 = root.add_child(
#             name="Test Category 3", description="Test Category description."
#         )

#         product = ProductFactory.create(
#             categories=(category_1, category_2, category_3)
#         )

#         assert product.categories.all().count() == 3

#     def test_brands_m2m(self):
#         """Tests the m2m relationship for
#         :py:attr:`~apps.products.models.product_models.Product.brands`.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         Product.objects.get(id=1).delete()

#         brand_1 = BrandFactory()
#         # TODO: Uncomment
#         # brand_2 = BrandFactory()
#         # brand_3 = BrandFactory()

#         # TODO: Add all 3
#         product = ProductFactory.create(brands=(brand_1,))

#         # TODO: Count 3
#         assert product.brands.all().count() == 1

#     def test_option_types_m2m(self):
#         """Tests the m2m relationship for
#         :py:attr:`~apps.products.models.product_models.Product.option_types`.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         Product.objects.get(id=1).delete()

#         option_type_1 = OptionTypeFactory()
#         # TODO: Uncomment
#         # option_type_2 = OptionTypeFactory()
#         # option_type_3 = OptionTypeFactory()

#         # TODO: Add all 3
#         product = ProductFactory.create(option_types=(option_type_1,))

#         # TODO: Count 3
#         assert product.option_types.all().count() == 1

#     # ----------------------------
#     # Custom Field Validator Tests
#     # ----------------------------
#     @pytest.mark.parametrize("test_price", [(0), (-0.01), (-10.23)])
#     def test_min_price_field_invalid_if_price_lower_than_minimum_specified(
#         self, test_price
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.min_price` is
#         invalid if below a specified minimum.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         Product.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "min_price": [
#                     f"Ensure this value is greater than or equal to {MIN_PRICE}."
#                 ],
#             },
#         ):
#             product = ProductFactory.create(
#                 min_price=Money(test_price, DEFAULT_CURRENCY)
#             )

#     @pytest.mark.parametrize("test_price", [0, -0.01, -10.23])
#     def test_max_price_field_invalid_if_price_lower_than_minimum_specified(
#         self, test_price
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.max_price` is
#         invalid if below a specified minimum.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         Product.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "max_price": [
#                     f"Ensure this value is greater than or equal to {MIN_PRICE}."
#                 ],
#             },
#         ):
#             product = ProductFactory.create(
#                 max_price=Money(test_price, DEFAULT_CURRENCY)
#             )

#     @pytest.mark.parametrize("test_price", [(0), (-0.01), (-10.23)])
#     def test_min_price_original_field_invalid_if_price_lower_than_minimum_specified(
#         self, test_price
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.min_price_original` is
#         invalid if below a specified minimum.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         Product.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "min_price_original": [
#                     f"Ensure this value is greater than or equal to {MIN_PRICE}."
#                 ],
#             },
#         ):
#             product = ProductFactory.create(
#                 min_price_original=Money(test_price, DEFAULT_CURRENCY)
#             )

#     @pytest.mark.parametrize("test_price", [(0), (-0.01), (-10.23)])
#     def test_max_price_original_field_invalid_if_price_lower_than_minimum_specified(
#         self, test_price
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.max_price_original` is
#         invalid if below a specified minimum.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         Product.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "max_price_original": [
#                     f"Ensure this value is greater than or equal to {MIN_PRICE}."
#                 ],
#             },
#         ):
#             product = ProductFactory.create(
#                 max_price_original=Money(test_price, DEFAULT_CURRENCY)
#             )

#     # ----------
#     # Meta Tests
#     # ----------
#     def test_ordering(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Product` objects
#         are ordered by appropriate attribute(s)."""
#         product = Product.objects.get(id=1)

#         assert product._meta.ordering == ("name",)

#     def test_verbose_name(self):
#         """Tests that the ``verbose_name`` of the
#         :py:model:`~apps.products.models.product_models.Product` model
#         is as expected.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.verbose_name == "Product"

#     def test_verbose_name_plural(self):
#         """Tests that the ``verbose_name_plural`` of the
#         :py:model:`~apps.products.models.product_models.Product` model
#         is as expected.
#         """
#         product = Product.objects.get(id=1)

#         assert product._meta.verbose_name_plural == "Products"

#     # -------------------
#     # Custom Method Tests
#     # -------------------
#     def test_get_absolute_url(self):
#         """Tests that the
#         :py:meth:`~apps.products.models.product_models.Product.get_absolute_url`
#         method returns expected URL.
#         """

#         product = Product.objects.get(id=1)

#         assert (
#             product.get_absolute_url() == f"/products/product/{product.slug}/"
#         )

#     def test_str(self):
#         """Tests that the string representation of
#         :py:model:`~apps.products.models.product_models.Product`
#         object is as expected.
#         """
#         product = Product.objects.get(id=1)

#         assert str(product) == f"{product.name}"

#     def test_as_dict(self):
#         """Tests that the dictionary representation of
#         :py:model:`~apps.products.models.product_models.Product`
#         object is as expected.
#         """
#         product = Product.objects.get(id=1)

#         categories = []
#         for category in product.categories.all():
#             categories.append(category._as_dict())

#         brands = []
#         for brand in product.brands.all():
#             brands.append(brand._as_dict())

#         option_types = []
#         for option_type in product.option_types.all():
#             option_types.append(option_type._as_dict())

#         expected_repr = {
#             "name": product.name,
#             "slug": product.slug,
#             "sku_symbol": product.sku_symbol,
#             "categories": categories,
#             "brands": brands,
#             "description": product.description,
#             "option_types": option_types,
#             "is_flagged": product.is_flagged,
#             "created": str(product.created),
#             "updated": str(product.updated),
#             "min_price": getattr(product.min_price, "amount"),
#             "min_price_currency": getattr(product.min_price, "currency"),
#             "max_price": getattr(product.max_price, "amount"),
#             "max_price_currency": getattr(product.max_price, "currency"),
#             "min_price_original": getattr(
#                 product.min_price_original, "amount"
#             ),
#             "min_price_original_currency": getattr(
#                 product.min_price_original, "currency"
#             ),
#             "max_price_original": getattr(
#                 product.max_price_original, "amount"
#             ),
#             "max_price_original_currency": getattr(
#                 product.max_price_original, "currency"
#             ),
#             "is_form_validated": product.is_form_validated,
#         }

#         assert product._as_dict() == expected_repr


# # ==========================
# # ProductVariant Model Tests
# # ==========================
# @pytest.mark.django_db
# class TestProductVariantModel(ValidationErrorTestMixin):
#     """Tests for the ProductVariant model."""

#     @pytest.fixture(autouse=True)
#     def setup_test_db(self, db):
#         """Sets up test database containing a basic
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant`
#         object
#         """
#         ProductVariantFactory()

#     # -----------
#     # Field Tests
#     # -----------
#     def test_product_variant_object_has_information_fields(self):
#         """Tests that
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant`
#         objects have correct number of fields and are populated
#         with values of the expected datatypes.
#         """

#         product_variant = ProductVariant.objects.get(id=1)

#         assert len(product_variant._meta.get_fields()) == 17
#         assert isinstance(product_variant.product, Product)
#         assert product_variant.option_values.model == OptionValue
#         assert isinstance(product_variant.stock, int)
#         assert isinstance(product_variant.selling_price, Money)
#         assert isinstance(product_variant.supplier, Supplier)
#         assert isinstance(product_variant.discounted_price, Money)
#         assert isinstance(product_variant.percentage_discount, Decimal)
#         assert isinstance(product_variant.created, datetime.datetime)
#         assert isinstance(product_variant.updated, datetime.datetime)
#         assert isinstance(product_variant.sku_no, str)
#         assert isinstance(product_variant.product_variant_summary, dict)
#         assert isinstance(product_variant.is_form_validated, bool)

#     def test_product_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.product`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert (
#             getattr(
#                 product_variant._meta.get_field("product").remote_field,
#                 "on_delete",
#                 None,
#             )
#             == models.CASCADE
#         )

#     def test_option_values_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.option_values`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert product_variant._meta.get_field("option_values").blank
#         assert (
#             product_variant._meta.get_field(
#                 "option_values"
#             ).related_query_name()
#             == "product_variants"
#         )

#     def test_supplier_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.supplier`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert (
#             getattr(
#                 product_variant._meta.get_field("supplier").remote_field,
#                 "on_delete",
#                 None,
#             )
#             == models.SET_NULL
#         )
#         assert product_variant._meta.get_field("supplier").blank
#         assert product_variant._meta.get_field("supplier").null

#     def test_stock_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.stock`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert product_variant._meta.get_field("stock").default == 0

#     def test_selling_price_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.selling_price`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert (
#             product_variant._meta.get_field("selling_price").max_digits == 19
#         )
#         assert (
#             product_variant._meta.get_field("selling_price").decimal_places
#             == CURRENCY_DP
#         )
#         assert (
#             product_variant._meta.get_field("selling_price").default_currency
#             == DEFAULT_CURRENCY
#         )

#     def test_discounted_price_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Product.discounted_price`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert (
#             product_variant._meta.get_field("discounted_price").max_digits
#             == 19
#         )
#         assert (
#             product_variant._meta.get_field("discounted_price").decimal_places
#             == CURRENCY_DP
#         )
#         assert (
#             product_variant._meta.get_field(
#                 "discounted_price"
#             ).default_currency
#             == DEFAULT_CURRENCY
#         )

#     def test_percentage_discount_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert (
#             product_variant._meta.get_field("percentage_discount").max_digits
#             == 4
#         )
#         assert (
#             product_variant._meta.get_field(
#                 "percentage_discount"
#             ).decimal_places
#             == PERCENTAGE_DISCOUNT_DP
#         )
#         assert product_variant._meta.get_field("percentage_discount").null
#         assert product_variant._meta.get_field("percentage_discount").blank

#     def test_created_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.created`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert product_variant._meta.get_field("created").auto_now_add

#     def test_updated_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.updated`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert product_variant._meta.get_field("updated").auto_now

#     def test_sku_no_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.sku_no`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert (
#             product_variant._meta.get_field("sku_no").max_length
#             == MAX_SKU_LENGTH
#         )
#         assert product_variant._meta.get_field("sku_no").unique

#     def test_product_variant_summary_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`
#         has the appropriate field attribute values.
#         """
#         # Nothing to test
#         pass

#     def test_is_form_validated_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.is_form_validated`
#         has the appropriate field attribute values.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert not product_variant._meta.get_field("is_form_validated").default

#     # ----------------------
#     # M2m Relationship Tests
#     # ----------------------
#     def test_option_values_m2m(self):
#         """Tests the m2m relationship for
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.option_values`.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         option_value_1 = OptionValueFactory()
#         # TODO: Uncomment
#         # option_value_2 = OptionValueFactory()
#         # option_value_3 = OptionValueFactory()

#         # TODO: Add all 3
#         product_variant = ProductVariantFactory.create(
#             option_values=(option_value_1,)
#         )

#         # TODO: Count 3
#         assert product_variant.option_values.all().count() == 1

#     # ----------------------------
#     # Custom Field Validator Tests
#     # ----------------------------
#     @pytest.mark.parametrize("test_price", [0, -0.01, -10.23])
#     def test_selling_price_field_invalid_if_price_lower_than_minimum_specified(
#         self, test_price
#     ):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.selling_price` is
#         invalid if below a specified minimum.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         # Price of 0 will actually cause other errors so as long as an error
#         # is raised, model will not be saved, therefore test passed.
#         try:
#             with self.assertModelFieldValidationErrors(
#                 self,
#                 {
#                     "selling_price": [
#                         f"Ensure this value is greater than or equal to {MIN_PRICE}."
#                     ],
#                     "__all__": [
#                         "Conflict between discounted price and percentage discount"
#                     ],
#                 },
#             ):
#                 product_variant = ProductVariantFactory.create(
#                     selling_price=Money(test_price, DEFAULT_CURRENCY)
#                 )

#         except DivisionByZero as e:
#             assert True

#     @pytest.mark.parametrize("test_price", [-0.01, -10.23])
#     def test_discounted_price_field_invalid_if_price_lower_than_minimum_specified(
#         self, test_price
#     ):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.discounted_price`
#         is invalid if below a specified minimum.

#         Note:
#             No need to actually test
#             :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.discounted_price`
#             being 0 as in the previous test because
#             :py:meth:`~apps.product_variants.models.product_variant_models.ProductVariant.save`
#             considers 0 to be a blank field.
#         """
#         # TODO: Remove
#         # Delete so that there is no duplicate because dataset is small
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "discounted_price": [
#                     f"Ensure this value is greater than or equal to {MIN_PRICE}."
#                 ],
#                 "__all__": [
#                     "Conflict between discounted price and percentage discount"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 discounted_price=Money(test_price, DEFAULT_CURRENCY)
#             )

#     @pytest.mark.parametrize(
#         "test_percentage_discount",
#         [
#             Decimal(-100.9).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             Decimal(-0.9).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             Decimal(-10.2).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#         ],
#     )
#     def test_percentage_discount_invalid_if_lower_than_minimum_specified(
#         self, test_percentage_discount
#     ):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#         is invalid if below a specified minimum.

#         Note:
#             No need to actually test
#             :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#             being 0
#             :py:meth:`~apps.product_variants.models.product_variant_models.ProductVariant.save`
#             considers 0 to be a blank field.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "percentage_discount": [
#                     f"Percentage discount cannot be less than {MIN_PERCENTAGE_DISCOUNT}"
#                 ],
#                 "__all__": [
#                     "Conflict between discounted price and percentage discount"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 percentage_discount=test_percentage_discount
#             )

#     @pytest.mark.parametrize(
#         "test_percentage_discount",
#         [
#             Decimal(90.1).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             Decimal(100).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             Decimal(110.2).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#         ],
#     )
#     def test_percentage_discount_invalid_if_higher_than_maximum_specified(
#         self, test_percentage_discount
#     ):
#         """Tests that
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#         is invalid if above a specified maximum.

#         Note:
#             No need to actually test
#             :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#             being 0
#             :py:meth:`~apps.product_variants.models.product_variant_models.ProductVariant.save`
#             considers 0 to be a blank field.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "percentage_discount": [
#                     f"Percentage discount cannot be greater than {MAX_PERCENTAGE_DISCOUNT}"
#                 ],
#                 "__all__": [
#                     "Conflict between discounted price and percentage discount"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 percentage_discount=test_percentage_discount
#             )

#     def test_product_variant_summary_invalid_if_missing_sku_no(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`
#         is invalid if missing ``sku_no``.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'sku_no' has been specified in the product variant summary"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 product_variant_summary={
#                     "name": "Nike Air Huarache",
#                     "categories": ["Men-Shoes-Lifestyle"],
#                     "option_values": ["6"],
#                     "created": "Thu Nov 18 11:18:56 2021",
#                 }
#             )

#     def test_product_variant_summary_invalid_if_missing_name(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`
#         is invalid if missing ``name``.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'name' has been specified in the product variant summary"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 product_variant_summary={
#                     "sku_no": "AHR-6",
#                     "categories": ["Men-Shoes-Lifestyle"],
#                     "option_values": ["6"],
#                     "created": "Thu Nov 18 11:18:56 2021",
#                 }
#             )

#     def test_product_variant_summary_invalid_if_missing_at_least_one_category(
#         self,
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`
#         is invalid if missing or empty ``categories``.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'categories' have been specified in the product variant summary"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 product_variant_summary={
#                     "sku_no": "AHR-6",
#                     "name": "Nike Air Huarache",
#                     "option_values": ["6"],
#                     "created": "Thu Nov 18 11:18:56 2021",
#                 }
#             )

#     def test_product_variant_summary_invalid_if_missing_created(
#         self,
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`
#         is invalid if missing ``created``.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'created' has been specified in the product variant summary"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 product_variant_summary={
#                     "sku_no": "AHR-6",
#                     "name": "Nike Air Huarache",
#                     "categories": ["Men-Shoes-Lifestyle"],
#                     "option_values": ["6"],
#                 }
#             )

#     # ----------
#     # Meta Tests
#     # ----------
#     def test_ordering(self):
#         """Tests that
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant` objects
#         are ordered by appropriate attribute(s)."""
#         product_variant = ProductVariant.objects.get(id=1)

#         assert product_variant._meta.order_with_respect_to.name == "product"

#     def test_verbose_name(self):
#         """Tests that the ``verbose_name`` of the
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant` model
#         is as expected.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert product_variant._meta.verbose_name == "Product Variant"

#     def test_verbose_name_plural(self):
#         """Tests that the ``verbose_name_plural`` of the
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant` model
#         is as expected.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert product_variant._meta.verbose_name_plural == "Product Variants"

#     # -------------------
#     # Custom Method Tests
#     # -------------------
#     def test_str(self):
#         """Tests that the string representation of
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant`
#         object is as expected.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         assert (
#             str(product_variant)
#             == f"{product_variant.product.name}-{product_variant.sku_no}"
#         )

#     def test_as_dict(self):
#         """Tests that the dictionary representation of
#         :py:model:`~apps.products.models.product_models.ProductVariant`
#         object is as expected.
#         """
#         product_variant = ProductVariant.objects.get(id=1)

#         option_values = []
#         for option_value in product_variant.option_values.all():
#             option_values.append(option_value._as_dict())

#         expected_repr = {
#             "product": product_variant.product._as_dict(),
#             "option_values": option_values,
#             "supplier": product_variant.supplier._as_dict(),
#             "stock": product_variant.stock,
#             "selling_price": getattr(product_variant.selling_price, "amount"),
#             "selling_price_currency": getattr(
#                 product_variant.selling_price, "currency"
#             ),
#             "discounted_price": getattr(
#                 product_variant.discounted_price, "amount"
#             ),
#             "discounted_price_currency": getattr(
#                 product_variant.discounted_price, "currency"
#             ),
#             "percentage_discount": product_variant.percentage_discount,
#             "created": str(product_variant.created),
#             "updated": str(product_variant.updated),
#             "sku_no": product_variant.sku_no,
#             "product_variant_summary": product_variant.product_variant_summary,
#             "is_form_validated": product_variant.is_form_validated,
#         }

#         assert product_variant._as_dict() == expected_repr

#     # ------------------
#     # Clean Method Tests
#     # ------------------
#     @pytest.mark.parametrize(
#         "test_discounted_price, test_percentage_discount",
#         [
#             (
#                 Decimal(0.01).quantize(CURRENCY_PRECISION),
#                 Decimal(32).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#             (
#                 Decimal(130.01).quantize(CURRENCY_PRECISION),
#                 Decimal(12).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#             (
#                 Decimal(44.0).quantize(CURRENCY_PRECISION),
#                 Decimal(12).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#         ],
#     )
#     def test_model_invalid_if_conflict_between_discounted_price_and_percentage_discount(
#         self, test_discounted_price, test_percentage_discount
#     ):
#         """
#         Tests that
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant`
#         is invalid if there is a conflict between
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.discounted_price`
#         and
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "__all__": [
#                     "Conflict between discounted price and percentage discount"
#                 ],
#             },
#         ):
#             product_variant = ProductVariantFactory.create(
#                 discounted_price=Money(
#                     test_discounted_price, DEFAULT_CURRENCY
#                 ),
#                 percentage_discount=test_percentage_discount,
#             )

#     @pytest.mark.parametrize(
#         "test_selling_price, test_discounted_price",
#         [
#             (
#                 Decimal(0.01).quantize(CURRENCY_PRECISION),
#                 Decimal(0.01).quantize(CURRENCY_PRECISION),
#             ),
#             (
#                 Decimal(130.01).quantize(CURRENCY_PRECISION),
#                 Decimal(130.5).quantize(CURRENCY_PRECISION),
#             ),
#             (
#                 Decimal(44.0).quantize(CURRENCY_PRECISION),
#                 Decimal(1002.7).quantize(CURRENCY_PRECISION),
#             ),
#         ],
#     )
#     def test_model_invalid_if_discounted_price_greater_or_equal_to_selling_price(
#         self, test_selling_price, test_discounted_price
#     ):
#         """
#         Tests that
#         :py:model:`~apps.product_variants.models.product_variant_models.ProductVariant`
#         is invalid if
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.discounted_price`
#         is greater or equal to
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.selling_price`.
#         """
#         # TODO: Remove delete statements
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         # try:
#         #     with self.assertModelFieldValidationErrors(
#         #         self,
#         #         {
#         #             "__all__": [
#         #                 "Discounted price cannot be greater or equal to selling price"
#         #             ],
#         #         },
#         #     ):
#         #         product_variant = ProductVariantFactory.create(
#         #             selling_price=Money(test_selling_price, DEFAULT_CURRENCY),
#         #             discounted_price=Money(test_discounted_price, DEFAULT_CURRENCY),
#         #             percentage_discount=Decimal(
#         #                 100 - (100 * (test_discounted_price / test_selling_price))
#         #             ).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#         #         )

#         # except AssertionError as e:
#         #     with self.assertModelFieldValidationErrors(
#         #         self,
#         #         {
#         #             "percentage_discount": [
#         #                 f"Percentage discount cannot be less than {MIN_PERCENTAGE_DISCOUNT}"
#         #             ],
#         #         },
#         #     ):
#         #         product_variant = ProductVariantFactory.create(
#         #             selling_price=Money(test_selling_price, DEFAULT_CURRENCY),
#         #             discounted_price=Money(
#         #                 test_discounted_price, DEFAULT_CURRENCY
#         #             ),
#         #             percentage_discount=Decimal(
#         #                 100
#         #                 - (100 * (test_discounted_price / test_selling_price))
#         #             ).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#         #         )

#     # -----------------
#     # Save Method Tests
#     # -----------------
#     @pytest.mark.parametrize(
#         "test_selling_price, test_discounted_price, test_percentage_discount",
#         [
#             (
#                 Decimal(0.02).quantize(CURRENCY_PRECISION),
#                 Decimal(0.01).quantize(CURRENCY_PRECISION),
#                 Decimal(50).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#             (
#                 Decimal(130.01).quantize(CURRENCY_PRECISION),
#                 Decimal(120.5).quantize(CURRENCY_PRECISION),
#                 Decimal(7.3).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#             (
#                 Decimal(44.0).quantize(CURRENCY_PRECISION),
#                 Decimal(13.7).quantize(CURRENCY_PRECISION),
#                 Decimal(68.9).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#         ],
#     )
#     def test_percentage_discount_populated_correctly_if_not_already(
#         self,
#         test_selling_price,
#         test_discounted_price,
#         test_percentage_discount,
#     ):
#         """Tests that if
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#         is not populated already and
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.discounted_price`
#         is, it is populated correctly based on
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.selling_price`
#         and
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.discounted_price`
#         """
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         product_variant = ProductVariantFactory.create(
#             selling_price=Money(test_selling_price, DEFAULT_CURRENCY),
#             discounted_price=Money(test_discounted_price, DEFAULT_CURRENCY),
#             percentage_discount=None,
#         )

#         assert product_variant.percentage_discount == test_percentage_discount

#     @pytest.mark.parametrize(
#         "test_selling_price, test_discounted_price, test_percentage_discount",
#         [
#             (
#                 Decimal(0.02).quantize(CURRENCY_PRECISION),
#                 Decimal(0.01).quantize(CURRENCY_PRECISION),
#                 Decimal(50).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#             (
#                 Decimal(130.01).quantize(CURRENCY_PRECISION),
#                 Decimal(120.52).quantize(CURRENCY_PRECISION),
#                 Decimal(7.3).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#             (
#                 Decimal(44.0).quantize(CURRENCY_PRECISION),
#                 Decimal(13.68).quantize(CURRENCY_PRECISION),
#                 Decimal(68.9).quantize(PERCENTAGE_DISCOUNT_PRECISION),
#             ),
#         ],
#     )
#     def test_discounted_price_populated_correctly_if_not_already(
#         self,
#         test_selling_price,
#         test_discounted_price,
#         test_percentage_discount,
#     ):
#         """Tests that if
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.discounted_price`
#         is not populated already and
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#         is, it is populated correctly based on
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.selling_price`
#         and
#         :py:attr:`~apps.product_variants.models.product_variant_models.ProductVariant.percentage_discount`
#         """
#         ProductVariant.objects.get(id=1).delete()
#         Product.objects.get(id=1).delete()
#         Supplier.objects.get(id=1).delete()
#         Sku.objects.get(id=1).delete()

#         product_variant = ProductVariantFactory.create(
#             selling_price=Money(test_selling_price, DEFAULT_CURRENCY),
#             discounted_price=None,
#             percentage_discount=test_percentage_discount,
#         )

#         assert product_variant.discounted_price.amount == test_discounted_price


# # ===============
# # Tag Model Tests
# # ===============
# @pytest.mark.django_db
# class TestTagModel:
#     """Tests for the Tag model."""

#     @pytest.fixture(autouse=True)
#     def setup_test_db(self, db):
#         """Sets up test database containing a basic
#         :py:model:`~apps.products.models.product_models.Tag` object
#         """
#         TagFactory()

#     # -----------
#     # Field Tests
#     # -----------
#     def test_tag_object_has_information_fields(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Tag`
#         objects have correct number of fields and are populated
#         with values of the expected datatypes.
#         """
#         tag = Tag.objects.get(id=1)

#         assert len(tag._meta.get_fields()) == 5
#         assert isinstance(tag.name, str)
#         assert isinstance(tag.product, Product)
#         assert isinstance(tag.created, datetime.datetime)
#         assert isinstance(tag.updated, datetime.datetime)

#     def test_name_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Tag.name`
#         has the appropriate field attribute values.
#         """
#         tag = Tag.objects.get(id=1)

#         assert tag._meta.get_field("name").max_length == 100

#     def test_product_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Tag.product`
#         has the appropriate field attribute values.
#         """
#         tag = Tag.objects.get(id=1)

#         assert (
#             getattr(
#                 tag._meta.get_field("product").remote_field,
#                 "on_delete",
#                 None,
#             )
#             == models.CASCADE
#         )

#     def test_created_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Tag.created`
#         has the appropriate field attribute values.
#         """
#         tag = Tag.objects.get(id=1)

#         assert tag._meta.get_field("created").auto_now_add

#     def test_updated_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Tag.updated`
#         has the appropriate field attribute values.
#         """
#         tag = Tag.objects.get(id=1)

#         assert tag._meta.get_field("updated").auto_now

#     # ----------
#     # Meta Tests
#     # ----------
#     def test_ordering(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Tag` objects
#         are ordered by appropriate attribute(s)."""

#         tag = Tag.objects.get(id=1)

#         assert tag._meta.ordering == ("name",)

#     def test_verbose_name(self):
#         """Tests that the ``verbose_name`` of the
#         :py:model:`~apps.products.models.product_models.Tag` model
#         is as expected.
#         """

#         tag = Tag.objects.get(id=1)

#         assert tag._meta.verbose_name == "Tag"

#     def test_verbose_name_plural(self):
#         """Tests that the ``verbose_name_plural`` of the
#         :py:model:`~apps.products.models.product_models.Tag` model
#         is as expected.
#         """

#         tag = Tag.objects.get(id=1)

#         assert tag._meta.verbose_name_plural == "Tags"

#     # -------------------
#     # Custom Method Tests
#     # -------------------
#     def test_str(self):
#         """Tests that the string representation of
#         :py:model:`~apps.products.models.product_models.Tag`
#         object is as expected.
#         """
#         tag = Tag.objects.get(id=1)

#         assert str(tag) == f"{tag.name}-{tag.product.slug}"

#     def test_as_dict(self):
#         """Tests that the dictionary representation of
#         :py:model:`~apps.products.models.product_models.Tag`
#         object is as expected.
#         """
#         tag = Tag.objects.get(id=1)

#         expected_repr = {
#             "name": tag.name,
#             "product": tag.product._as_dict(),
#             "created": str(tag.created),
#             "updated": str(tag.updated),
#         }

#         assert tag._as_dict() == expected_repr

#     # -----------------
#     # Save Method Tests
#     # -----------------
#     @pytest.mark.parametrize(
#         "test_name, expected_test_name",
#         [
#             ("TEST TAG ALL CAPS", "test tag all caps"),
#             ("TesT Tag SOmE CAps", "test tag some caps"),
#             (
#                 "#T3S+ +^g 5PeC!al c#^raC+3&S\n",
#                 "#t3s+ +^g 5pec!al c#^rac+3&s\n",
#             ),
#         ],
#     )
#     def test_name_converted_to_lowercase(self, test_name, expected_test_name):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Tag.name`
#         is converted to lowercase.
#         """
#         # TODO: Remove
#         Product.objects.get(id=1).delete()

#         tag = TagFactory.create(name=test_name)

#         assert tag.name == expected_test_name


# # ===============
# # Sku Model Tests
# # ===============
# @pytest.mark.django_db
# class TestSkuModel(ValidationErrorTestMixin):
#     """Tests for the Sku model."""

#     @pytest.fixture(autouse=True)
#     def setup_test_db(self, db):
#         """Sets up test database containing a basic
#         :py:model:`~apps.products.models.product_models.Sku` object
#         """
#         SkuFactory()

#     # -----------
#     # Field Tests
#     # -----------
#     def test_sku_object_has_information_fields(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Sku`
#         objects have correct number of fields and are populated
#         with values of the expected datatypes.
#         """
#         sku = Sku.objects.get(id=1)

#         assert len(sku._meta.get_fields()) == 5
#         assert isinstance(sku.sku_no, str)
#         assert isinstance(sku.product_variant_summary, dict)
#         assert isinstance(sku.created, datetime.datetime)
#         assert isinstance(sku.updated, datetime.datetime)

#     def test_sku_no_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.sku_no`
#         has the appropriate field attribute values.
#         """
#         sku = Sku.objects.get(id=1)

#         assert sku._meta.get_field("sku_no").max_length == MAX_SKU_LENGTH
#         assert sku._meta.get_field("sku_no").unique

#     def test_product_variant_summary_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.product_variant_summary`
#         has the appropriate field attribute values.
#         """
#         pass

#     def test_created_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.created`
#         has the appropriate field attribute values.
#         """
#         sku = Sku.objects.get(id=1)

#         assert sku._meta.get_field("created").auto_now_add

#     def test_updated_at_field_attributes(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.updated`
#         has the appropriate field attribute values.
#         """
#         sku = Sku.objects.get(id=1)

#         assert sku._meta.get_field("updated").auto_now

#     # ----------
#     # Meta Tests
#     # ----------
#     def test_ordering(self):
#         """Tests that
#         :py:model:`~apps.products.models.product_models.Sku` objects
#         are ordered by appropriate attribute(s)."""

#         sku = Sku.objects.get(id=1)

#         assert sku._meta.ordering == ("sku_no",)

#     def test_verbose_name(self):
#         """Tests that the ``verbose_name`` of the
#         :py:model:`~apps.products.models.product_models.Sku` model
#         is as expected.
#         """

#         sku = Sku.objects.get(id=1)

#         assert sku._meta.verbose_name == "SKU"

#     def test_verbose_name_plural(self):
#         """Tests that the ``verbose_name_plural`` of the
#         :py:model:`~apps.products.models.product_models.Sku` model
#         is as expected.
#         """

#         sku = Sku.objects.get(id=1)

#         assert sku._meta.verbose_name_plural == "SKUs"

#     # ----------------------------
#     # Custom Field Validator Tests
#     # ----------------------------
#     def test_product_variant_summary_invalid_if_missing_sku_no(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.product_variant_summary`
#         is invalid if missing ``sku_no``.
#         """
#         # TODO: Remove
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'sku_no' has been specified in the product variant summary"
#                 ],
#             },
#         ):
#             sku = SkuFactory.create(
#                 product_variant_summary={
#                     "name": "Nike Air Huarache",
#                     "categories": ["Men-Shoes-Lifestyle"],
#                     "option_values": ["6"],
#                     "created": "Thu Nov 18 11:18:56 2021",
#                 }
#             )

#     def test_product_variant_summary_invalid_if_missing_name(self):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.product_variant_summary`
#         is invalid if missing ``name``.
#         """
#         # TODO: Remove
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'name' has been specified in the product variant summary"
#                 ],
#             },
#         ):
#             sku = SkuFactory.create(
#                 product_variant_summary={
#                     "sku_no": "AHR-6",
#                     "categories": ["Men-Shoes-Lifestyle"],
#                     "option_values": ["6"],
#                     "created": "Thu Nov 18 11:18:56 2021",
#                 }
#             )

#     def test_product_variant_summary_invalid_if_missing_at_least_one_category(
#         self,
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.product_variant_summary`
#         is invalid if missing or empty ``categories``.
#         """
#         # TODO: Remove
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'categories' have been specified in the product variant summary"
#                 ],
#             },
#         ):
#             sku = SkuFactory.create(
#                 product_variant_summary={
#                     "sku_no": "AHR-6",
#                     "name": "Nike Air Huarache",
#                     "option_values": ["6"],
#                     "created": "Thu Nov 18 11:18:56 2021",
#                 }
#             )

#     def test_product_variant_summary_invalid_if_missing_created(
#         self,
#     ):
#         """Tests that
#         :py:attr:`~apps.products.models.product_models.Sku.product_variant_summary`
#         is invalid if missing ``created``.
#         """
#         # TODO: Remove
#         Sku.objects.get(id=1).delete()

#         with self.assertModelFieldValidationErrors(
#             self,
#             {
#                 "product_variant_summary": [
#                     "Ensure that 'created' has been specified in the product variant summary"
#                 ],
#             },
#         ):
#             sku = SkuFactory.create(
#                 product_variant_summary={
#                     "sku_no": "AHR-6",
#                     "name": "Nike Air Huarache",
#                     "categories": ["Men-Shoes-Lifestyle"],
#                     "option_values": ["6"],
#                 }
#             )

#     # -------------------
#     # Custom Method Tests
#     # -------------------
#     def test_str(self):
#         """Tests that the string representation of
#         :py:model:`~apps.products.models.product_models.Sku`
#         object is as expected.
#         """
#         sku = Sku.objects.get(id=1)

#         assert str(sku) == f"{sku.sku_no}"

#     def test_as_dict(sku):
#         """Tests that the dictionary representation of
#         :py:model:`~apps.products.models.product_models.Sku`
#         object is as expected.
#         """
#         sku = Sku.objects.get(id=1)

#         expected_repr = {
#             "sku_no": sku.sku_no,
#             "product_variant_summary": sku.product_variant_summary,
#             "created": str(sku.created),
#             "updated": str(sku.updated),
#         }

#         assert sku._as_dict() == expected_repr
