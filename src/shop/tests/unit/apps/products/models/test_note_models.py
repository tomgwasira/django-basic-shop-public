#!/usr/bin/env python
"""Tests for models defined in
:py:mod:`~apps.products.models.note_models`.
"""

# Standard library imports
import datetime

# Django library imports
from django.urls import reverse

# Third party library imports
import pytest

# Local application imports
from apps.products.models.note_models import *
from apps.products.models.product_models import *

from tests.factories.products.note_models_factories import *
from tests.mixins import ValidationErrorTestMixin


# =====================
# BasicNote Model Tests
# =====================
@pytest.mark.django_db
class TestBasicNoteModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.BasicNote`.
    """

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.BasicNote` object
        """
        BasicNoteFactory()

    # -----------
    # Field Tests
    # -----------
    def test_basic_note_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.BasicNote`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        basic_note = BasicNote.objects.get(id=1)

        assert len(basic_note._meta.get_fields()) == 11
        assert isinstance(basic_note.note, str)
        assert isinstance(basic_note.is_displayed_on_dashboard, bool)
        assert isinstance(basic_note.created, datetime.datetime)
        assert isinstance(basic_note.updated, datetime.datetime)

    def test_note_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.BasicNote.name`
        has the appropriate field attribute values.
        """
        basic_note = BasicNote.objects.get(id=1)

        assert basic_note._meta.get_field("note").max_length == 1000
        assert basic_note._meta.get_field("note").blank

    def test_is_displayed_on_dashboard_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.product_models.BasicNote.is_displayed_on_dashboard`
        has the appropriate field attribute values.
        """
        basic_note = BasicNote.objects.get(id=1)

        assert not basic_note._meta.get_field(
            "is_displayed_on_dashboard"
        ).default

    def test_created_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.BasicNote.created`
        has the appropriate field attribute values.
        """
        basic_note = BasicNote.objects.get(id=1)

        assert basic_note._meta.get_field("created").auto_now_add

    def test_updated_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.BasicNote.updated`
        has the appropriate field attribute values.
        """
        basic_note = BasicNote.objects.get(id=1)

        assert basic_note._meta.get_field("updated").auto_now

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.BasicNote` objects
        are ordered by appropriate attribute(s)."""

        basic_note = BasicNote.objects.get(id=1)

        assert basic_note._meta.ordering == ("updated",)

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_models.BasicNote` model
        is as expected.
        """

        basic_note = BasicNote.objects.get(id=1)

        assert basic_note._meta.verbose_name == "Basic Note"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_models.BasicNote` model
        is as expected.
        """

        basic_note = BasicNote.objects.get(id=1)

        assert basic_note._meta.verbose_name_plural == "Basic Notes"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_models.BasicNote`
        object is as expected.
        """
        basic_note = BasicNote.objects.get(id=1)

        assert str(basic_note) == f"basic-note-{basic_note.id}"

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_models.BasicNote`
        object is as expected.
        """
        basic_note = BasicNote.objects.get(id=1)

        expected_repr = {
            "note": basic_note.note,
            "is_displayed_on_dashboard": basic_note.is_displayed_on_dashboard,
            "created": str(basic_note.created),
            "updated": str(basic_note.updated),
        }

        assert basic_note._as_dict() == expected_repr


# ========================
# CategoryNote Model Tests
# ========================
@pytest.mark.django_db
class TestCategoryNoteModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.CategoryNote`."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.CategoryNote` object
        """

        CategoryNoteFactory()

    # -----------
    # Field Tests
    # -----------
    def test_category_note_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.CategoryNote`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        category_note = CategoryNote.objects.get(id=1)

        assert len(category_note._meta.get_fields()) == 9
        assert isinstance(category_note.note, str)
        assert isinstance(category_note.category, Category)
        assert isinstance(category_note.is_displayed_on_dashboard, bool)
        assert isinstance(category_note.created, datetime.datetime)
        assert isinstance(category_note.updated, datetime.datetime)

    def test_note_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.CategoryNote.name`
        has the appropriate field attribute values.
        """
        category_note = CategoryNote.objects.get(id=1)

        assert category_note._meta.get_field("note").max_length == 1000
        assert category_note._meta.get_field("note").blank

    def test_category_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.CategoryNote.category`
        has the appropriate field attribute values.
        """
        category_note = CategoryNote.objects.get(id=1)

        assert (
            getattr(
                category_note._meta.get_field("category").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_is_displayed_on_dashboard_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.product_models.CategoryNote.is_displayed_on_dashboard`
        has the appropriate field attribute values.
        """
        category_note = CategoryNote.objects.get(id=1)

        assert not category_note._meta.get_field(
            "is_displayed_on_dashboard"
        ).default

    def test_created_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.CategoryNote.created`
        has the appropriate field attribute values.
        """
        category_note = CategoryNote.objects.get(id=1)

        assert category_note._meta.get_field("created").auto_now_add

    def test_updated_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.CategoryNote.updated`
        has the appropriate field attribute values.
        """
        category_note = CategoryNote.objects.get(id=1)

        assert category_note._meta.get_field("updated").auto_now

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.CategoryNote` objects
        are ordered by appropriate attribute(s)."""

        category_note = CategoryNote.objects.get(id=1)

        assert category_note._meta.order_with_respect_to.name == "category"

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_models.CategoryNote` model
        is as expected.
        """

        category_note = CategoryNote.objects.get(id=1)

        assert category_note._meta.verbose_name == "Category Note"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_models.CategoryNote` model
        is as expected.
        """

        category_note = CategoryNote.objects.get(id=1)

        assert category_note._meta.verbose_name_plural == "Category Notes"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_models.CategoryNote`
        object is as expected.
        """
        category_note = CategoryNote.objects.get(id=1)

        assert (
            str(category_note)
            == f"category-note-{category_note.category.name}"
        )

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_models.CategoryNote`
        object is as expected.
        """
        category_note = CategoryNote.objects.get(id=1)

        expected_repr = {
            "note": category_note.note,
            "category": category_note.category._as_dict(),
            "is_displayed_on_dashboard": category_note.is_displayed_on_dashboard,
            "created": str(category_note.created),
            "updated": str(category_note.updated),
        }

        assert category_note._as_dict() == expected_repr


# ==========================
# OptionTypeNote Model Tests
# ==========================
@pytest.mark.django_db
class TestOptionTypeNoteModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.OptionTypeNote`."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.OptionTypeNote` object
        """

        OptionTypeNoteFactory()

    # -----------
    # Field Tests
    # -----------
    def test_option_type_note_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.OptionTypeNote`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        assert len(option_type_note._meta.get_fields()) == 9
        assert isinstance(option_type_note.note, str)
        assert isinstance(option_type_note.option_type, OptionType)
        assert isinstance(option_type_note.is_displayed_on_dashboard, bool)
        assert isinstance(option_type_note.created, datetime.datetime)
        assert isinstance(option_type_note.updated, datetime.datetime)

    def test_note_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.OptionTypeNote.name`
        has the appropriate field attribute values.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        assert option_type_note._meta.get_field("note").max_length == 1000
        assert option_type_note._meta.get_field("note").blank

    def test_option_type_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.OptionTypeNote.option_type`
        has the appropriate field attribute values.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        assert (
            getattr(
                option_type_note._meta.get_field("option_type").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_is_displayed_on_dashboard_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.product_models.OptionTypeNote.is_displayed_on_dashboard`
        has the appropriate field attribute values.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        assert not option_type_note._meta.get_field(
            "is_displayed_on_dashboard"
        ).default

    def test_created_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.OptionTypeNote.created`
        has the appropriate field attribute values.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        assert option_type_note._meta.get_field("created").auto_now_add

    def test_updated_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.OptionTypeNote.updated`
        has the appropriate field attribute values.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        assert option_type_note._meta.get_field("updated").auto_now

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.OptionTypeNote` objects
        are ordered by appropriate attribute(s)."""

        option_type_note = OptionTypeNote.objects.get(id=1)

        assert (
            option_type_note._meta.order_with_respect_to.name == "option_type"
        )

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_models.OptionTypeNote` model
        is as expected.
        """

        option_type_note = OptionTypeNote.objects.get(id=1)

        assert option_type_note._meta.verbose_name == "Option Type Note"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_models.OptionTypeNote` model
        is as expected.
        """

        option_type_note = OptionTypeNote.objects.get(id=1)

        assert (
            option_type_note._meta.verbose_name_plural == "Option Type Notes"
        )

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_models.OptionTypeNote`
        object is as expected.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        assert (
            str(option_type_note)
            == f"option_type-note-{option_type_note.option_type.name}"
        )

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_models.OptionTypeNote`
        object is as expected.
        """
        option_type_note = OptionTypeNote.objects.get(id=1)

        expected_repr = {
            "note": option_type_note.note,
            "option_type": option_type_note.option_type._as_dict(),
            "is_displayed_on_dashboard": option_type_note.is_displayed_on_dashboard,
            "created": str(option_type_note.created),
            "updated": str(option_type_note.updated),
        }

        assert option_type_note._as_dict() == expected_repr


# =====================
# BrandNote Model Tests
# =====================
@pytest.mark.django_db
class TestBrandNoteModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.BrandNote`."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.BrandNote` object
        """

        BrandNoteFactory()

    # -----------
    # Field Tests
    # -----------
    def test_brand_note_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.BrandNote`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        brand_note = BrandNote.objects.get(id=1)

        assert len(brand_note._meta.get_fields()) == 9
        assert isinstance(brand_note.note, str)
        assert isinstance(brand_note.brand, Brand)
        assert isinstance(brand_note.is_displayed_on_dashboard, bool)
        assert isinstance(brand_note.created, datetime.datetime)
        assert isinstance(brand_note.updated, datetime.datetime)

    def test_note_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.BrandNote.name`
        has the appropriate field attribute values.
        """
        brand_note = BrandNote.objects.get(id=1)

        assert brand_note._meta.get_field("note").max_length == 1000
        assert brand_note._meta.get_field("note").blank

    def test_brand_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.BrandNote.brand`
        has the appropriate field attribute values.
        """
        brand_note = BrandNote.objects.get(id=1)

        assert (
            getattr(
                brand_note._meta.get_field("brand").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_is_displayed_on_dashboard_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.product_models.BrandNote.is_displayed_on_dashboard`
        has the appropriate field attribute values.
        """
        brand_note = BrandNote.objects.get(id=1)

        assert not brand_note._meta.get_field(
            "is_displayed_on_dashboard"
        ).default

    def test_created_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.BrandNote.created`
        has the appropriate field attribute values.
        """
        brand_note = BrandNote.objects.get(id=1)

        assert brand_note._meta.get_field("created").auto_now_add

    def test_updated_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.BrandNote.updated`
        has the appropriate field attribute values.
        """
        brand_note = BrandNote.objects.get(id=1)

        assert brand_note._meta.get_field("updated").auto_now

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.BrandNote` objects
        are ordered by appropriate attribute(s)."""

        brand_note = BrandNote.objects.get(id=1)

        assert brand_note._meta.order_with_respect_to.name == "brand"

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_models.BrandNote` model
        is as expected.
        """

        brand_note = BrandNote.objects.get(id=1)

        assert brand_note._meta.verbose_name == "Brand Note"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_models.BrandNote` model
        is as expected.
        """

        brand_note = BrandNote.objects.get(id=1)

        assert brand_note._meta.verbose_name_plural == "Brand Notes"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_models.BrandNote`
        object is as expected.
        """
        brand_note = BrandNote.objects.get(id=1)

        assert str(brand_note) == f"brand-note-{brand_note.brand.name}"

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_models.BrandNote`
        object is as expected.
        """
        brand_note = BrandNote.objects.get(id=1)

        expected_repr = {
            "note": brand_note.note,
            "brand": brand_note.brand._as_dict(),
            "is_displayed_on_dashboard": brand_note.is_displayed_on_dashboard,
            "created": str(brand_note.created),
            "updated": str(brand_note.updated),
        }

        assert brand_note._as_dict() == expected_repr


# ========================
# SupplierNote Model Tests
# ========================
@pytest.mark.django_db
class TestSupplierNoteModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.SupplierNote`."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.SupplierNote` object
        """

        SupplierNoteFactory()

    # -----------
    # Field Tests
    # -----------
    def test_supplier_note_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.SupplierNote`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        assert len(supplier_note._meta.get_fields()) == 9
        assert isinstance(supplier_note.note, str)
        assert isinstance(supplier_note.supplier, Supplier)
        assert isinstance(supplier_note.is_displayed_on_dashboard, bool)
        assert isinstance(supplier_note.created, datetime.datetime)
        assert isinstance(supplier_note.updated, datetime.datetime)

    def test_note_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.SupplierNote.name`
        has the appropriate field attribute values.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        assert supplier_note._meta.get_field("note").max_length == 1000
        assert supplier_note._meta.get_field("note").blank

    def test_supplier_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.SupplierNote.supplier`
        has the appropriate field attribute values.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        assert (
            getattr(
                supplier_note._meta.get_field("supplier").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_is_displayed_on_dashboard_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.product_models.SupplierNote.is_displayed_on_dashboard`
        has the appropriate field attribute values.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        assert not supplier_note._meta.get_field(
            "is_displayed_on_dashboard"
        ).default

    def test_created_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.SupplierNote.created`
        has the appropriate field attribute values.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        assert supplier_note._meta.get_field("created").auto_now_add

    def test_updated_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.SupplierNote.updated`
        has the appropriate field attribute values.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        assert supplier_note._meta.get_field("updated").auto_now

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.SupplierNote` objects
        are ordered by appropriate attribute(s)."""

        supplier_note = SupplierNote.objects.get(id=1)

        assert supplier_note._meta.order_with_respect_to.name == "supplier"

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_models.SupplierNote` model
        is as expected.
        """

        supplier_note = SupplierNote.objects.get(id=1)

        assert supplier_note._meta.verbose_name == "Supplier Note"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_models.SupplierNote` model
        is as expected.
        """

        supplier_note = SupplierNote.objects.get(id=1)

        assert supplier_note._meta.verbose_name_plural == "Supplier Notes"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_models.SupplierNote`
        object is as expected.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        assert (
            str(supplier_note)
            == f"supplier-note-{supplier_note.supplier.name}"
        )

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_models.SupplierNote`
        object is as expected.
        """
        supplier_note = SupplierNote.objects.get(id=1)

        expected_repr = {
            "note": supplier_note.note,
            "supplier": supplier_note.supplier._as_dict(),
            "is_displayed_on_dashboard": supplier_note.is_displayed_on_dashboard,
            "created": str(supplier_note.created),
            "updated": str(supplier_note.updated),
        }

        assert supplier_note._as_dict() == expected_repr


# ========================
# ProductNote Model Tests
# ========================
@pytest.mark.django_db
class TestProductNoteModel:
    """Tests for
    :py:model:`~apps.products.models.note_models.ProductNote`."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.ProductNote` object
        """

        ProductNoteFactory()

    # -----------
    # Field Tests
    # -----------
    def test_product_note_object_has_information_fields(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.ProductNote`
        objects have correct number of fields and are populated
        with values of the expected datatypes.
        """
        product_note = ProductNote.objects.get(id=1)

        assert len(product_note._meta.get_fields()) == 9
        assert isinstance(product_note.note, str)
        assert isinstance(product_note.product, Product)
        assert isinstance(product_note.is_displayed_on_dashboard, bool)
        assert isinstance(product_note.created, datetime.datetime)
        assert isinstance(product_note.updated, datetime.datetime)

    def test_note_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductNote.name`
        has the appropriate field attribute values.
        """
        product_note = ProductNote.objects.get(id=1)

        assert product_note._meta.get_field("note").max_length == 1000
        assert product_note._meta.get_field("note").blank

    def test_product_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductNote.product`
        has the appropriate field attribute values.
        """
        product_note = ProductNote.objects.get(id=1)

        assert (
            getattr(
                product_note._meta.get_field("product").remote_field,
                "on_delete",
                None,
            )
            == models.CASCADE
        )

    def test_is_displayed_on_dashboard_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.product_models.ProductNote.is_displayed_on_dashboard`
        has the appropriate field attribute values.
        """
        product_note = ProductNote.objects.get(id=1)

        assert not product_note._meta.get_field(
            "is_displayed_on_dashboard"
        ).default

    def test_created_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductNote.created`
        has the appropriate field attribute values.
        """
        product_note = ProductNote.objects.get(id=1)

        assert product_note._meta.get_field("created").auto_now_add

    def test_updated_field_attributes(self):
        """Tests that
        :py:attr:`~apps.products.models.note_models.ProductNote.updated`
        has the appropriate field attribute values.
        """
        product_note = ProductNote.objects.get(id=1)

        assert product_note._meta.get_field("updated").auto_now

    # ----------
    # Meta Tests
    # ----------
    def test_ordering(self):
        """Tests that
        :py:model:`~apps.products.models.product_models.ProductNote` objects
        are ordered by appropriate attribute(s)."""

        product_note = ProductNote.objects.get(id=1)

        assert product_note._meta.order_with_respect_to.name == "product"

    def test_verbose_name(self):
        """Tests that the ``verbose_name`` of the
        :py:model:`~apps.products.models.product_models.ProductNote` model
        is as expected.
        """

        product_note = ProductNote.objects.get(id=1)

        assert product_note._meta.verbose_name == "Product Note"

    def test_verbose_name_plural(self):
        """Tests that the ``verbose_name_plural`` of the
        :py:model:`~apps.products.models.product_models.ProductNote` model
        is as expected.
        """

        product_note = ProductNote.objects.get(id=1)

        assert product_note._meta.verbose_name_plural == "Product Notes"

    # -------------------
    # Custom Method Tests
    # -------------------
    def test_str(self):
        """Tests that the string representation of
        :py:model:`~apps.products.models.product_models.ProductNote`
        object is as expected.
        """
        product_note = ProductNote.objects.get(id=1)

        assert str(product_note) == f"product-note-{product_note.product.name}"

    def test_repr(self):
        """Tests that the dictionary representation of
        :py:model:`~apps.products.models.product_models.ProductNote`
        object is as expected.
        """
        product_note = ProductNote.objects.get(id=1)

        expected_repr = {
            "note": product_note.note,
            "product": product_note.product._as_dict(),
            "is_displayed_on_dashboard": product_note.is_displayed_on_dashboard,
            "created": str(product_note.created),
            "updated": str(product_note.updated),
        }

        assert product_note._as_dict() == expected_repr
