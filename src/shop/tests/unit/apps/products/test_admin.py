#!/usr/bin/env python
""" Tests for admin of *Products* app."""

# Standard library imports
import datetime

# Django library imports
from django.contrib.admin.sites import AdminSite
from django.forms import inlineformset_factory
from django.http import QueryDict

# Third-party library imports
import pytest

# Local application imports
from apps.products.admin import *
from apps.products.models import *

from tests.factories.products.product_models_factories import (
    BrandFactory,
    OptionTypeFactory,
    OptionValueFactory,
    ProductFactory,
    ProductVariantFactory,
    SupplierFactory,
    SkuFactory,
)


__author__ = "Thomas Gwasira"
__date__ = "October 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


# ===================
# CategoryAdmin Tests
# ===================
@pytest.mark.django_db
class TestCategoryAdmin:
    """Tests for :py:class:`~apps.products.admin.CategoryAdmin`."""

    # ------------------
    # Setup and Teardown
    # ------------------
    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.Category` object
        as well as ``AdminSite``.
        """
        root = Category.add_root()
        root.add_child(
            name="Test Category", description="Test Category description."
        )

        self.site = AdminSite()
        self.category_admin = CategoryAdmin(Category, self.site)

    # -----------
    # Field Tests
    # -----------
    def test_add_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.CategoryAdmin`
        add form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        assert list(self.category_admin.get_form(request).base_fields) == [
            "name",
            "description",
            "_position",
            "_ref_node_id",
        ]
        assert list(self.category_admin.get_fields(request)) == [
            "name",
            "description",
            "_position",
            "_ref_node_id",
        ]

        # No excluded fields
        assert not self.category_admin.get_exclude(request)

    def test_change_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.CategoryAdmin`
        change form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        category = Category.objects.get(id=2)

        assert list(
            self.category_admin.get_form(request, category).base_fields
        ) == [
            "name",
            "description",
            "_position",
            "_ref_node_id",
        ]
        assert list(self.category_admin.get_fields(request, category)) == [
            "name",
            "description",
            "_position",
            "_ref_node_id",
        ]

        # No excluded fields
        assert not self.category_admin.get_exclude(request, category)

    # ------------
    # Inline Tests
    # ------------
    def test_correct_number_of_inlines(self):
        """Tests that :py:class:`~apps.products.admin.CategoryAdmin` has
        the expected number of inlines.
        """
        inline_instances = self.category_admin.get_inline_instances(
            request, self.category_admin
        )

        assert len(inline_instances) == 2

    def test_category_hero_image_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.CategoryHeroImageInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.image_models.CategoryHeroImage`
        model and has all expected fields.
        """
        category_hero_image_inline_instance = (
            self.category_admin.get_inline_instances(
                request, self.category_admin
            )[0]
        )

        assert isinstance(
            category_hero_image_inline_instance, CategoryHeroImageInline
        )
        assert category_hero_image_inline_instance.model == CategoryHeroImage
        assert list(
            list(self.category_admin.get_formsets_with_inlines(request))[0][
                0
            ]()
            .forms[0]
            .fields
        ) == ["image", "category", "index", "id", "DELETE"]

    def test_category_note_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.CategoryNoteInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.note_models.CategoryNote`
        model and has all expected fields.
        """
        category_note_inline_instance = (
            self.category_admin.get_inline_instances(
                request, self.category_admin
            )[1]
        )

        assert isinstance(category_note_inline_instance, CategoryNoteInline)
        assert category_note_inline_instance.model == CategoryNote

        assert list(
            list(self.category_admin.get_formsets_with_inlines(request))[1][
                0
            ]()
            .forms[0]
            .fields
        ) == [
            "note",
            "is_displayed_on_dashboard",
            "category",
            "basicnote_ptr",
        ]

    def test_category_note_inline_delete_permission_is_false(self):
        """Tests that delete permission for
        :py:class:`~apps.products.admin.CategoryNoteInline` is False.
        """
        category_note_inline_instance = (
            self.category_admin.get_inline_instances(
                request, self.category_admin
            )[1]
        )

        assert not category_note_inline_instance.has_delete_permission(request)


# ===============
# OptionTypeAdmin
# ===============
class TestOptionTypeAdmin:
    """Tests for :py:class:`~apps.products.admin.OptionTypeAdmin`."""

    # ------------------
    # Setup and Teardown
    # ------------------
    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.OptionType`
        :py:model:`~apps.products.models.product_models.OptionValue`
        objects as well as ``AdminSite``.
        """
        # Creates OptionType in the process
        OptionValueFactory()

        self.site = AdminSite()
        self.option_type_admin = OptionTypeAdmin(OptionType, self.site)

    def test_add_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.OptionTypeAdmin`
        add form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        assert list(self.option_type_admin.get_form(request).base_fields) == [
            "name",
            "display_name",
            "index",
            "description",
        ]
        assert list(self.option_type_admin.get_fields(request)) == [
            "name",
            "display_name",
            "index",
            "description",
        ]

        # No excluded fields
        assert not self.option_type_admin.get_exclude(request)

    def test_change_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.OptionTypeAdmin`
        change form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        option_type = OptionType.objects.get(id=1)

        assert list(
            self.option_type_admin.get_form(request, option_type).base_fields
        ) == [
            "name",
            "display_name",
            "index",
            "description",
        ]
        assert list(
            self.option_type_admin.get_fields(request, option_type)
        ) == ["name", "display_name", "index", "description"]

        # No excluded fields
        assert not self.option_type_admin.get_exclude(request, option_type)

    def test_correct_number_of_inlines(self):
        """Tests that :py:class:`~apps.products.admin.OptionTypeAdmin` has
        the expected number of inlines.
        """
        inline_instances = self.option_type_admin.get_inline_instances(
            request, self.option_type_admin
        )

        assert len(inline_instances) == 2

    def test_option_value_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.OptionValueInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.product_models.OptionValue`
        model and has all expected fields.
        """
        option_value_inline_instance = (
            self.option_type_admin.get_inline_instances(
                request, self.option_type_admin
            )[0]
        )

        assert isinstance(
            option_value_inline_instance, OptionValueOptionTypeInline
        )
        assert option_value_inline_instance.model == OptionValue
        assert list(
            list(self.option_type_admin.get_formsets_with_inlines(request))[0][
                0
            ]()
            .forms[0]
            .fields
        ) == [
            "value",
            "unit",
            "display_symbol",
            "sku_symbol",
            "option_type",
            "id",
            "DELETE",
        ]

    def test_option_type_note_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.OptionTypeNoteInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.note_models.OptionTypeNote`
        model and has all expected fields.
        """
        option_type_note_inline_instance = (
            self.option_type_admin.get_inline_instances(
                request, self.option_type_admin
            )[1]
        )

        assert isinstance(
            option_type_note_inline_instance, OptionTypeNoteInline
        )
        assert option_type_note_inline_instance.model == OptionTypeNote

        assert list(
            list(self.option_type_admin.get_formsets_with_inlines(request))[1][
                0
            ]()
            .forms[0]
            .fields
        ) == [
            "note",
            "is_displayed_on_dashboard",
            "option_type",
            "basicnote_ptr",
        ]

    def test_option_type_note_inline_delete_permission_is_false(self):
        """Tests that delete permission for
        :py:class:`~apps.products.admin.OptionTypeNoteInline` is False.
        """
        option_type_note_inline_instance = (
            self.option_type_admin.get_inline_instances(
                request, self.option_type_admin
            )[1]
        )

        assert not option_type_note_inline_instance.has_delete_permission(
            request
        )


# ================
# BrandAdmin Tests
# ================
class TestBrandAdmin:
    """Tests for :py:class:`~apps.products.admin.BrandAdmin`."""

    # ------------------
    # Setup and Teardown
    # ------------------
    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.Brand`
        object as well as ``AdminSite``.
        """
        BrandFactory()

        self.site = AdminSite()
        self.brand_admin = BrandAdmin(Brand, self.site)

    def test_add_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.BrandAdmin`
        add form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        assert list(self.brand_admin.get_form(request).base_fields) == [
            "name",
            "index",
        ]
        assert list(self.brand_admin.get_fields(request)), ["name", "index"]

        # No excluded fields
        assert not self.brand_admin.get_exclude(request)

    def test_change_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.BrandAdmin`
        change form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        brand = Brand.objects.get(id=1)

        assert list(self.brand_admin.get_form(request, brand).base_fields) == [
            "name",
            "index",
        ]
        assert list(self.brand_admin.get_fields(request, brand)) == [
            "name",
            "index",
        ]

        # No excluded fields
        assert not self.brand_admin.get_exclude(request, brand)

    def test_correct_number_of_inlines(self):
        """Tests that :py:class:`~apps.products.admin.BrandAdmin` has
        the expected number of inlines.
        """
        self.brand_admin = BrandAdmin(Brand, self.site)
        inline_instances = self.brand_admin.get_inline_instances(
            request, self.brand_admin
        )

        assert len(inline_instances) == 1

    def test_brand_note_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.BrandNoteInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.note_models.BrandNote`
        model and has all expected fields.
        """
        self.brand_admin = BrandAdmin(Brand, self.site)
        brand_note_inline_instance = self.brand_admin.get_inline_instances(
            request, self.brand_admin
        )[0]

        assert isinstance(brand_note_inline_instance, BrandNoteInline)
        assert brand_note_inline_instance.model == BrandNote

        assert list(
            list(self.brand_admin.get_formsets_with_inlines(request))[0][0]()
            .forms[0]
            .fields
        ) == ["note", "is_displayed_on_dashboard", "brand", "basicnote_ptr"]

    def test_brand_note_inline_delete_permission_is_false(self):
        """Tests that delete permission for
        :py:class:`~apps.products.admin.OptionTypeNoteInline` is False.
        """
        self.brand_admin = BrandAdmin(Brand, self.site)
        brand_note_inline_instance = self.brand_admin.get_inline_instances(
            request, self.brand_admin
        )[0]

        assert not brand_note_inline_instance.has_delete_permission(request)


# ===================
# SupplierAdmin Tests
# ===================
class TestSupplierAdmin:
    """Tests for :py:class:`~apps.products.admin.SupplierAdmin`."""

    # ------------------
    # Setup and Teardown
    # ------------------
    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.Supplier`
        object as well as ``AdminSite``.
        """
        SupplierFactory()

        self.site = AdminSite()
        self.supplier_admin = SupplierAdmin(Supplier, self.site)

    def test_add_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.SupplierAdmin`
        add form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        assert list(self.supplier_admin.get_form(request).base_fields) == [
            "name",
            "details",
        ]
        assert list(self.supplier_admin.get_fields(request)), [
            "name",
            "details",
        ]

        # No excluded fields
        assert not self.supplier_admin.get_exclude(request)

    def test_change_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.SupplierAdmin`
        change form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        supplier = Supplier.objects.get(id=1)

        assert list(
            self.supplier_admin.get_form(request, supplier).base_fields
        ) == [
            "name",
            "details",
        ]
        assert list(self.supplier_admin.get_fields(request, supplier)) == [
            "name",
            "details",
        ]

        # No excluded fields
        assert not self.supplier_admin.get_exclude(request, supplier)

    def test_correct_number_of_inlines(self):
        """Tests :py:class:`~apps.products.admin.SupplierAdmin` has
        the expected number of inlines.
        """
        self.supplier_admin = SupplierAdmin(Supplier, self.site)
        inline_instances = self.supplier_admin.get_inline_instances(
            request, self.supplier_admin
        )

        assert len(inline_instances) == 1

    def test_supplier_note_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.SupplierNoteInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.note_models.SupplierNote`
        model and has all expected fields.
        """
        self.supplier_admin = SupplierAdmin(Supplier, self.site)
        supplier_note_inline_instance = (
            self.supplier_admin.get_inline_instances(
                request, self.supplier_admin
            )[0]
        )

        assert isinstance(supplier_note_inline_instance, SupplierNoteInline)
        assert supplier_note_inline_instance.model == SupplierNote

        assert list(
            list(self.supplier_admin.get_formsets_with_inlines(request))[0][
                0
            ]()
            .forms[0]
            .fields
        ) == ["note", "is_displayed_on_dashboard", "supplier", "basicnote_ptr"]

    def test_supplier_note_inline_delete_permission_is_false(self):
        """Tests that delete permission for
        :py:class:`~apps.products.admin.OptionTypeNoteInline` is False.
        """
        self.supplier_admin = SupplierAdmin(Supplier, self.site)
        supplier_note_inline_instance = (
            self.supplier_admin.get_inline_instances(
                request, self.supplier_admin
            )[0]
        )

        assert not supplier_note_inline_instance.has_delete_permission(request)


# ==================
# ProductAdmin Tests
# ==================
class TestProductAdmin:
    """Tests for :py:class:`~apps.products.admin.ProductAdmin`."""

    # ------------------
    # Setup and Teardown
    # ------------------
    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing basic
        :py:model:`~apps.products.models.product_models.OptionType`,
        :py:model:`~apps.products.models.product_models.OptionValue`,
        :py:model:`~apps.products.models.product_models.Product` and
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects as well as ``AdminSite``.

        Comment:
            *   Some of the objects created in this method are only used later
                on in the tests. It would have been ideal to create them in the
                test methods that use them; however, in the interest of efficiency,
                they will only be created once here.
            *   Objects in this test database are class attributes so that they
                can be referred to without needing to query the test database.
                This ensures no id errors are made during querying.
        """
        # Categories
        # For some reason, the django-treebeard admin page creates
        # the first object having pk=1 i.e. it behaves as the root
        # similar to what is done below
        self.category_1 = Category.add_root(
            name="Category 1", description="Test Category description."
        )
        self.category_1_1 = self.category_1.add_child(
            name="Category 1_1", description="Test Category description."
        )
        self.category_1_2 = self.category_1.add_child(
            name="Category 1_2", description="Test Category description."
        )
        self.category_1_1_1 = self.category_1_1.add_child(
            name="Category 1_1_1", description="Test Category description."
        )

        # Product
        self.product = ProductFactory()

        # ProductVariant
        self.product_variant = ProductVariantFactory(product=self.product)

        # TODO: Remove arguments to factories
        # OptionTypes
        option_type_1 = OptionTypeFactory.create(name="Test OptionType 1")
        option_type_2 = OptionTypeFactory.create(name="Test OptionType 2")
        option_type_3 = OptionTypeFactory.create(name="Test OptionType 3")

        # TODO: Remove arguments to factories
        # OptionValues
        self.option_value_1_1 = OptionValueFactory.create(
            option_type=option_type_1, sku_symbol="ABC"
        )
        self.option_value_1_2 = OptionValueFactory.create(
            option_type=option_type_1, sku_symbol="DEF"
        )

        self.option_value_2_1 = OptionValueFactory.create(
            option_type=option_type_2, sku_symbol="GHI"
        )
        self.option_value_2_2 = OptionValueFactory.create(
            option_type=option_type_2, sku_symbol="JKL"
        )

        self.option_value_3_1 = OptionValueFactory.create(
            option_type=option_type_3, sku_symbol="MNO"
        )
        self.option_value_3_2 = OptionValueFactory.create(
            option_type=option_type_3, sku_symbol="PQR"
        )

        # TODO: Remove arguments to factories
        # Supplier
        self.supplier_1 = SupplierFactory.create(name="Test Supplier 1")
        self.supplier_2 = SupplierFactory.create(name="Test Supplier 2")

        self.site = AdminSite()
        self.product_admin = ProductAdmin(Product, self.site)

    # -----------
    # Field Tests
    # -----------
    # ~~~~~~~~~~~~
    # ProductAdmin
    # ~~~~~~~~~~~~
    def test_add_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.ProductAdmin`
        add form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        assert list(self.product_admin.get_form(request).base_fields) == [
            "name",
            "sku_symbol",
            "categories",
            "brands",
            "description",
            "option_types",
            "is_flagged",
        ]
        assert list(self.product_admin.get_fields(request)) == [
            "name",
            "sku_symbol",
            "categories",
            "brands",
            "description",
            "option_types",
            "is_flagged",
        ]
        assert list(self.product_admin.get_form(request)._meta.exclude) == [
            "min_price",
            "max_price",
            "min_price_original",
            "max_price_original",
            "is_form_validated",
        ]

    def test_change_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.ProductAdmin`
        change form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        product = Product.objects.get(id=1)

        assert list(
            self.product_admin.get_form(request, product).base_fields
        ) == [
            "name",
            "sku_symbol",
            "categories",
            "brands",
            "description",
            "option_types",
            "is_flagged",
        ]
        assert list(self.product_admin.get_fields(request, product)) == [
            "name",
            "sku_symbol",
            "categories",
            "brands",
            "description",
            "option_types",
            "is_flagged",
        ]
        assert list(
            self.product_admin.get_form(request, product)._meta.exclude
        ) == [
            "min_price",
            "max_price",
            "min_price_original",
            "max_price_original",
            "is_form_validated",
        ]

    def test_correct_number_of_inlines(self):
        """Tests that :py:class:`~apps.products.admin.ProductAdmin` has
        the expected number of inlines.
        """
        inline_instances = self.product_admin.get_inline_instances(
            request, self.product_admin
        )

        assert len(inline_instances) == 4

    def test_product_image_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.ProductImageInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.image_models.ProductImage`
        model and has all expected fields.
        """
        product_image_inline_instance = (
            self.product_admin.get_inline_instances(
                request, self.product_admin
            )[0]
        )

        assert isinstance(product_image_inline_instance, ProductImageInline)
        assert product_image_inline_instance.model == ProductImage
        assert list(
            list(self.product_admin.get_formsets_with_inlines(request))[0][0]()
            .forms[0]
            .fields
        ) == ["image", "product", "index", "id", "DELETE"]

    def test_tag_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.TagInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.product_models.Tag`
        model and has all expected fields.
        """
        tag_inline_instance = self.product_admin.get_inline_instances(
            request, self.product_admin
        )[1]

        assert isinstance(tag_inline_instance, TagInline)
        assert tag_inline_instance.model == Tag

        assert list(
            list(self.product_admin.get_formsets_with_inlines(request))[1][0]()
            .forms[0]
            .fields
        ) == ["name", "product", "id", "DELETE"]

    def test_product_note_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.ProductNoteInline` is in
        is in correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.note_models.ProductNote`
        model and has all expected fields.
        """
        product_note_inline_instance = self.product_admin.get_inline_instances(
            request, self.product_admin
        )[2]

        assert isinstance(product_note_inline_instance, ProductNoteInline)
        assert product_note_inline_instance.model == ProductNote
        assert list(
            list(self.product_admin.get_formsets_with_inlines(request))[2][0]()
            .forms[0]
            .fields
        ) == ["note", "is_displayed_on_dashboard", "product", "basicnote_ptr"]

    def test_product_note_inline_delete_permission_is_false(self):
        """Tests that delete permission for
        :py:class:`~apps.products.admin.ProductNoteInline` is False.
        """
        self.product_admin = ProductAdmin(Product, self.site)
        product_note_inline_instance = self.product_admin.get_inline_instances(
            request, self.product_admin
        )[2]

        assert not product_note_inline_instance.has_delete_permission(request)

    # ~~~~~~~~~~~~~~~~~~~~
    # ProductVariantInline
    # ~~~~~~~~~~~~~~~~~~~~
    def test_product_variant_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.ProductVariantInline` is in
        correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.product_models.ProductVariant`
        model and has all expected fields.
        """
        product_variant_inline = self.product_admin.get_inline_instances(
            request, self.product_admin
        )[3]

        assert isinstance(product_variant_inline, ProductVariantInline)
        assert product_variant_inline.model == ProductVariant
        assert product_variant_inline.min_num == 1
        assert product_variant_inline.extra == 0

        assert list(product_variant_inline.get_fields(request)) == [
            "product",
            "supplier",
            "stock",
            "selling_price",
            "discounted_price",
            "percentage_discount",
        ]
        assert list(product_variant_inline.get_exclude(request)) == [
            "sku_no",
            "product_variant_summary",
            "is_form_validated",
            "option_values",
        ]

    def test_correct_number_of_inlines_in_product_variant_inline(self):
        """Tests that :py:class:`~apps.products.admin.ProductVariantInline`
        has the expected number of inlines.
        """
        product_variant_inline = self.product_admin.get_inline_instances(
            request, self.product_admin
        )[3]
        product_variant_inline_inline_instances = (
            product_variant_inline.get_inline_instances(
                request, product_variant_inline
            )
        )

        assert len(product_variant_inline_inline_instances) == 2

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # OptionValueProductVariantInline
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_option_value_product_variant_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.OptionValueProductVariantInline` is in
        correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.product_models.OptionValue`
        model and has all expected fields.
        """
        self.product_admin = ProductAdmin(Product, self.site)
        product_variant_inline = self.product_admin.get_inline_instances(
            request, self.product_admin
        )[3]
        option_value_product_variant_inline = (
            product_variant_inline.get_inline_instances(request)[0]
        )

        assert isinstance(
            option_value_product_variant_inline,
            OptionValueProductVariantInline,
        )
        assert (
            option_value_product_variant_inline.model
            == ProductVariant.option_values.through
        )
        assert list(
            option_value_product_variant_inline.get_fields(request)
        ) == ["productvariant", "optionvalue"]

        assert (
            option_value_product_variant_inline.formset
            == OptionValueProductVariantInlineFormSet
        )
        assert option_value_product_variant_inline.extra == 0

        # No excluded fields
        assert not option_value_product_variant_inline.get_exclude(request)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # ProductVariantImageInline
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_product_variant_image_inline_corresponds_to_correct_model_and_has_expected_fields(
        self,
    ):
        """Tests that
        :py:class:`~apps.products.admin.ProductVariantImageInline` is in
        correct position in list of inlines, corresponds to
        :py:model:`~apps.products.models.image_models.ProductVariantImage`
        model and has all expected fields.
        """
        product_variant_inline = self.product_admin.get_inline_instances(
            request, self.product_admin
        )[3]
        product_variant_image_inline = (
            product_variant_inline.get_inline_instances(request)[1]
        )

        assert isinstance(
            product_variant_image_inline, ProductVariantImageInline
        )
        assert product_variant_image_inline.model == ProductVariantImage
        assert list(product_variant_image_inline.get_fields(request)) == [
            "image",
            "product_variant",
            "index",
        ]

        # No excluded fields
        assert not product_variant_image_inline.get_exclude(request)

    # ------------------
    # Clean Method Tests
    # ------------------
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # OptionValueProductVariantInlineFormset
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_sku_no_generation_single_option_value(self):
        """Tests that
        :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
        generates expected
        :py:attr:`~apps.products.models.product_models.ProductVariant.sku_no`
        when only a single
        :py:model:`~apps.products.models.product_models.OptionValue` is selected.

        Comment:
            ``extra=3`` implies that three additional blank
            :py:class:`apps.products.admin.OptionValueProductVariantInlineFormSet
            forms are being submitted just to ensure that everything works as
            expected if blank forms are added.
        """
        # Create test data to pass to formset
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
        )

        # Create formset
        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=3,
        )

        # Submit test data to formset and clean
        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        formset.is_valid()

        assert (
            formset.instance.sku_no
            == f"{self.product_variant.product.sku_symbol}-{self.option_value_1_1.sku_symbol}"
        )

    def test_generate_sku_no_multiple_option_values_multiple_option_types(
        self,
    ):
        """Tests that
        :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
        generates expected
        :py:attr:`~apps.products.models.product_models.ProductVariant.sku_no`
        when multiple
        :py:model:`~apps.products.models.product_models.OptionValue` objects each
        with a different related
        :py:model:`~apps.products.models.product_models.OptionType` object are
        selected.
        """
        # Create test data to pass to formset
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "option_types=3&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            # Accessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
            "ProductVariant_option_values-2-optionvalue=5&"
        )

        # Create formset
        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=0,
        )

        # Submit test data to formset and clean
        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        formset.is_valid()

        assert (
            formset.instance.sku_no
        ), f"{self.product_variant.product.sku_symbol}-{self.option_value_1_1.sku_symbol}-{self.option_value_2_1.sku_symbol}-{self.option_value_3_1.sku_symbol}"

    def test_generate_sku_no_first_generated_sku_no_already_exists(
        self,
    ):
        """Tests that
        :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
        generates expected
        :py:attr:`~apps.products.models.product_models.ProductVariant.sku_no`
        when a
        :py:model:`~apps.products.models.product_models.Sku` object with the
        first generated ``sku_no`` already exists.
        """
        # Create Sku object with same sku_no first generated by formset clean
        SkuFactory.create(
            sku_no=(
                f"{self.product_variant.product.sku_symbol}-{self.option_value_1_1.sku_symbol}-{self.option_value_2_1.sku_symbol}-{self.option_value_3_1.sku_symbol}"
            )
        )

        # Create test data to pass to formset
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "option_types=3&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
            "ProductVariant_option_values-2-optionvalue=5&"
        )

        # Create formset
        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=0,
        )

        # Submit test data to formset and clean
        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        formset.is_valid()

        assert (
            formset.instance.sku_no
        ), f"{self.product_variant.product.sku_symbol}-{self.option_value_1_1.sku_symbol}-{self.option_value_2_1.sku_symbol}-{self.option_value_3_1.sku_symbol}-2"

    def test_generate_sku_no_first_two_generated_sku_no_already_exists(
        self,
    ):
        """Tests that
        :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
        generates expected
        :py:attr:`~apps.products.models.product_models.ProductVariant.sku_no`
        when
        :py:model:`~apps.products.models.product_models.Sku` objects with the
        first and second generated ``sku_no``s already exist.
        """
        # Create Sku objects with same sku_no as first two generated by formset clean
        SkuFactory.create(
            sku_no=(
                f"{self.product_variant.product.sku_symbol}-{self.option_value_1_1.sku_symbol}-{self.option_value_2_1.sku_symbol}-{self.option_value_3_1.sku_symbol}"
            )
        )

        SkuFactory.create(
            sku_no=(
                f"{self.product_variant.product.sku_symbol}-{self.option_value_1_1.sku_symbol}-{self.option_value_2_1.sku_symbol}-{self.option_value_3_1.sku_symbol}-2"
            )
        )

        # Create test data to pass to formset
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "option_types=3&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
            "ProductVariant_option_values-2-optionvalue=5&"
        )

        # Create formset
        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=0,
        )

        # Submit test data to formset and clean
        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        formset.is_valid()

        assert (
            formset.instance.sku_no
        ), f"{self.product_variant.product.sku_symbol}-{self.option_value_1_1.sku_symbol}-{self.option_value_2_1.sku_symbol}-{self.option_value_3_1.sku_symbol}-3"

    def test_product_variant_summary_generation_single_option_value(self):
        """Tests that
        :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
        generates expected
        :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`
        when only a single
        :py:model:`~apps.products.models.product_models.OptionValue` is selected.

        Comment:
            ``extra=3`` implies that three additional blank
            :py:class:`apps.products.admin.OptionValueProductVariantInlineFormSet
            forms are being submitted just to ensure that everything works as
            expected if blank forms are added.
        """
        # Create test data to pass to formset
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
        )

        # Create formset
        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=3,
        )

        # Submit test data to formset and clean
        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        formset.is_valid()

        # Set up expected product_variant_summary
        ## Get all categories of Product
        categories = []
        for category in self.product_variant.product.categories.all():
            categories.append(category.name)

        ## Add all option values of ProductVariant supplied in data
        ## passed into formset
        option_values = [self.option_value_1_1.value]

        expected_product_variant_summary = {
            "sku_no": self.product_variant.sku_no,
            "name": self.product_variant.product.name,
            "categories": categories,
            "option_values": option_values,
            "created": self.product_variant.created.strftime("%c"),
        }

        assert (
            formset.instance.product_variant_summary
            == expected_product_variant_summary
        )

    def test_generate_product_variant_summary_multiple_option_values_multiple_option_types(
        self,
    ):
        """Tests that
        :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
        generates expected
        :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`
        when multiple
        :py:model:`~apps.products.models.product_models.OptionValue` objects each
        with a different related
        :py:model:`~apps.products.models.product_models.OptionType` object are
        selected.
        """
        # Create test data to pass to formset
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "option_types=3&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            # Accessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
            "ProductVariant_option_values-2-optionvalue=5&"
        )

        # Create formset
        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=0,
        )

        # Submit test data to formset and clean
        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        formset.is_valid()

        # Set up expected product_variant_summary
        ## Get all categories of Product
        categories = []
        for category in self.product_variant.product.categories.all():
            categories.append(category.name)

        ## Add all option values of ProductVariant supplied in data
        ## passed into formset
        option_values = [
            self.option_value_1_1.value,
            self.option_value_2_1.value,
            self.option_value_3_1.value,
        ]

        expected_product_variant_summary = {
            "sku_no": self.product_variant.sku_no,
            "name": self.product_variant.product.name,
            "categories": categories,
            "option_values": option_values,
            "created": self.product_variant.created.strftime("%c"),
        }

        assert (
            formset.instance.product_variant_summary
            == expected_product_variant_summary
        )

    def test_option_value_formset_invalid_if_same_option_value_selected_more_once(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.OptionValueProductVariantInlineFormSet`
        is invalid if an
        :py:model:`~apps.products.models.product_models.OptionValue` is selected
        more than once.
        """
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=3&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=1&"
            "ProductVariant_option_values-2-optionvalue=5&"
        )

        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=3,
        )

        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        assert not formset.is_valid()

        # Deliberately checking the specific error because there shouldn't be
        # more than one error
        assert len(formset.errors[1]["__all__"]) == 1
        assert (
            formset.errors[1]["__all__"][0]
            == "Please correct the duplicate values below."
        )

    def test_option_value_formset_invalid_if_an_option_type_has_no_option_value_specified(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.OptionValueProductVariantInlineFormSet`
        is invalid if an
        :py:model:`~apps.products.models.product_models.OptionType` has no
        corresponding
        :py:model:`~apps.products.models.product_models.OptionValue` selected.

        Comment:
            Validation is performed in
            :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
            The formset ``clean`` method is called after all the
            ``Form.clean`` methods have been called. The errors are
            found using the ``non_form_errors()`` method on the formset.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "option_types=3&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
        )

        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=3,
        )

        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        assert not formset.is_valid()

    def test_option_value_formset_invalid_if_two_option_values_of_same_option_type(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.OptionValueProductVariantInlineFormSet`
        is invalid if two
        :py:model:`~apps.products.models.product_models.OptionValues` of the
        same
        :py:model:`~apps.products.models.product_models.OptionType` were selected.

        Comment:
            Validation is performed in
            :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
            The formset ``clean`` method is called after all the
            ``Form.clean`` methods have been called. The errors are
            found using the ``non_form_errors()`` method on the formset.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "option_types=3&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=4&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
            "ProductVariant_option_values-2-optionvalue=4&"
        )

        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=0,
        )

        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        assert not formset.is_valid()

    def test_option_value_formset_invalid_if_both_an_option_type_has_no_option_value_specified_and_two_option_values_of_same_option_type(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.OptionValueProductVariantInlineFormSet`
        is invalid if an
        :py:model:`~apps.products.models.product_models.OptionType` has no
        :py:model:`~apps.products.models.product_models.OptionValue` selected
        and also, two
        :py:model:`~apps.products.models.product_models.OptionValues` of the
        same
        :py:model:`~apps.products.models.product_models.OptionType` were selected.

        Comment:
            Validation is performed in
            :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
            The formset ``clean`` method is called after all the
            ``Form.clean`` methods have been called. The errors are
            found using the ``non_form_errors()`` method on the formset.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """

        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=4&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
            "ProductVariant_option_values-2-optionvalue=4&"
        )

        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=0,
        )

        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        assert not formset.is_valid()

    def test_option_value_formset_invalid_if_additional_option_value_specified_beyond_option_types(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.OptionValueProductVariantInlineFormSet`
        is invalid if an additional
        :py:model:`~apps.products.models.product_models.OptionValue` is
        specified for which an
        :py:model:`~apps.products.models.product_models.OptionType`
        was not.

        Comment:
            Validation is performed in
            :py:meth:`apps.products.admin.OptionValueProductVariantInlineFormSet.clean`
            The formset ``clean`` method is called after all the
            ``Form.clean`` methods have been called. The errors are
            found using the ``non_form_errors()`` method on the formset.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Accessed through self.data
            "option_types=1&"
            "option_types=2&"
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            # Acessed through self.cleaned_data
            "ProductVariant_option_values-TOTAL_FORMS=3&"
            "ProductVariant_option_values-INITIAL_FORMS=0&"
            "ProductVariant_option_values-MAX_NUM_FORMS=1000&"
            "ProductVariant_option_values-0-optionvalue=1&"
            "ProductVariant_option_values-1-optionvalue=3&"
            "ProductVariant_option_values-2-optionvalue=5&"
        )

        OptionValueProductVariantInlineTestFormset = inlineformset_factory(
            ProductVariant,
            ProductVariant.option_values.through,
            formset=OptionValueProductVariantInlineFormSet,
            fields=["id", "productvariant", "optionvalue"],
            exclude=[],
            extra=0,
        )

        formset = OptionValueProductVariantInlineTestFormset(
            data, instance=self.product_variant
        )
        assert not formset.is_valid()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ProductVariantInlineFormset
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_product_form_invalid_if_both_parent_and_child_categories_selected(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.ProductForm`
        is invalid if both parent and child
        :py:model:`~apps.products.models.product_models.Category` objects
        are selected.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&categories=2&"
            # ProductVariant data (at least one ProductVariant is required)
            # (accessed through self.data)
            "productvariant_set-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=0&"
            "productvariant_set-0-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-0-selling_price_0=1.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
        )

        # Submit data to form and clean
        # Don't worry about adding a ProductVariant. It is completely
        # separate from the Product and the ProductForm
        form = ProductForm(data, instance=self.product)
        assert not form.is_valid()

    def test_product_form_valid_if_product_variants_have_different_option_value_sets_and_same_supplier(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.ProductForm`
        is invalid if data for at least two
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects has same sets of
        :py:model:`~apps.products.models.product_models.OptionValue`
        and same
        :py:model:`~apps.products.models.product_models.Supplier`

        In other words, it is invalid if user is attempting to
        create duplicate
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects.

        For this test,
        :py:model:`~apps.products.models.product_models.OptionValue`
        objects are 'selected' in different orders and the 'selected'
        :py:model:`~apps.products.models.product_models.Supplier`
        objects are the same.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&option_types=1&option_types=2&option_types=3&"
            # ProductVariant data (accessed through self.data)
            "productvariant_set-TOTAL_FORMS=2&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            "productvariant_set-0-ProductVariant_supplier-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_supplier=1&"
            "productvariant_set-0-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-0-selling_price_0=1.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
            "productvariant_set-1-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-1-ProductVariant_option_values-0-optionvalue=2&"
            "productvariant_set-1-ProductVariant_option_values-1-optionvalue=4&"
            "productvariant_set-1-ProductVariant_option_values-2-optionvalue=6&"
            "productvariant_set-1-ProductVariant_supplier-TOTAL_FORMS=1&"
            "productvariant_set-1-ProductVariant_supplier=1&"
            "productvariant_set-1-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-1-selling_price_0=1.00&"
            "productvariant_set-1-selling_price_1=ZAR&"
        )

        # Submit form and clean
        form = ProductForm(data, instance=self.product)
        assert form.is_valid()

    def test_product_form_valid_if_product_variants_have_same_option_value_sets_and_different_supplier(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.ProductForm`
        is invalid if data for at least two
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects has same sets of
        :py:model:`~apps.products.models.product_models.OptionValue`
        and same
        :py:model:`~apps.products.models.product_models.Supplier`

        In other words, it is invalid if user is attempting to
        create duplicate
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects.

        For this test,
        :py:model:`~apps.products.models.product_models.OptionValue`
        objects are 'selected' in different orders and the 'selected'
        :py:model:`~apps.products.models.product_models.Supplier`
        objects are the same.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&option_types=1&option_types=2&option_types=3&"
            # ProductVariant data (accessed through self.data)
            "productvariant_set-TOTAL_FORMS=2&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            "productvariant_set-0-ProductVariant_supplier-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_supplier=1&"
            "productvariant_set-0-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-0-selling_price_0=1.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
            "productvariant_set-1-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-1-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-1-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-1-ProductVariant_option_values-2-optionvalue=5&"
            "productvariant_set-1-ProductVariant_supplier-TOTAL_FORMS=1&"
            "productvariant_set-1-ProductVariant_supplier=2&"
            "productvariant_set-1-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-1-selling_price_0=1.00&"
            "productvariant_set-1-selling_price_1=ZAR&"
        )

        # Submit form and clean
        form = ProductForm(data, instance=self.product)
        assert form.is_valid()

    def test_product_form_invalid_if_product_variants_have_same_option_value_sets_with_same_order_and_no_supplier(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.ProductForm`
        is invalid if data for at least two
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects has same sets of
        :py:model:`~apps.products.models.product_models.OptionValue`
        and same
        :py:model:`~apps.products.models.product_models.Supplier`

        In other words, it is invalid if user is attempting to
        create duplicate
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects.

        For this test,
        :py:model:`~apps.products.models.product_models.OptionValue`
        objects are 'selected' in the same order and in both cases, there
        is not
        :py:model:`~apps.products.models.product_models.Supplier`
        'selected'.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&option_types=1&option_types=2&option_types=3&"
            # ProductVariant data (accessed through self.data)
            "productvariant_set-TOTAL_FORMS=2&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            "productvariant_set-0-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-0-selling_price_0=1.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
            "productvariant_set-1-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-1-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-1-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-1-ProductVariant_option_values-2-optionvalue=5&"
            "productvariant_set-1-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-1-selling_price_0=1.00&"
            "productvariant_set-1-selling_price_1=ZAR&"
        )

        # Submit form and clean
        form = ProductForm(data, instance=self.product)
        assert not form.is_valid()

    def test_product_form_invalid_if_product_variants_have_same_option_value_sets_in_different_order_and_same_supplier(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.ProductForm`
        is invalid if data for at least two
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects has same sets of
        :py:model:`~apps.products.models.product_models.OptionValue`
        and same
        :py:model:`~apps.products.models.product_models.Supplier`

        In other words, it is invalid if user is attempting to
        create duplicate
        :py:model:`~apps.products.models.product_models.ProductVariant`
        objects.

        For this test,
        :py:model:`~apps.products.models.product_models.OptionValue`
        objects are 'selected' in different orders and the 'selected'
        :py:model:`~apps.products.models.product_models.Supplier`
        objects are the same.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&option_types=1&option_types=2&option_types=3&"
            # ProductVariant data (accessed through self.data)
            "productvariant_set-TOTAL_FORMS=2&"
            "productvariant_set-0-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-0-ProductVariant_option_values-0-optionvalue=1&"
            "productvariant_set-0-ProductVariant_option_values-1-optionvalue=3&"
            "productvariant_set-0-ProductVariant_option_values-2-optionvalue=5&"
            "productvariant_set-0-ProductVariant_supplier-TOTAL_FORMS=1&"
            "productvariant_set-0-ProductVariant_supplier=1&"
            "productvariant_set-0-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-0-selling_price_0=1.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
            "productvariant_set-1-ProductVariant_option_values-TOTAL_FORMS=3&"
            "productvariant_set-1-ProductVariant_option_values-0-optionvalue=5&"
            "productvariant_set-1-ProductVariant_option_values-1-optionvalue=1&"
            "productvariant_set-1-ProductVariant_option_values-2-optionvalue=3&"
            "productvariant_set-1-ProductVariant_supplier-TOTAL_FORMS=1&"
            "productvariant_set-1-ProductVariant_supplier=1&"
            "productvariant_set-1-ProductVariant_selling_price-TOTAL_FORMS=1&"
            "productvariant_set-1-selling_price_0=1.00&"
            "productvariant_set-1-selling_price_1=ZAR&"
        )

        # Submit form and clean
        form = ProductForm(data, instance=self.product)
        assert not form.is_valid()

    def test_product_price_assignments_based_on_product_variant_inline_formset_no_discounts(
        self,
    ):
        """Tests that the prices for the instance of the
        :py:model:`~apps.products.models.product_models.Product`
        being created through the
        :py:meth:`apps.products.admin.ProductForm` have been assigned correctly.
        """
        data = QueryDict(
            # Accessed through self.data
            "productvariant_set-TOTAL_FORMS=5&"
            "productvariant_set-0-selling_price_0=2.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
            "productvariant_set-1-selling_price_0=5.30&"
            "productvariant_set-1-selling_price_1=ZAR&"
            "productvariant_set-2-selling_price_0=10.70&"
            "productvariant_set-2-selling_price_1=ZAR&"
            "productvariant_set-3-selling_price_0=4.20&"
            "productvariant_set-3-selling_price_1=ZAR&"
            "productvariant_set-4-selling_price_0=0.02&"
            "productvariant_set-4-selling_price_1=ZAR&"
            # Accessed through self.cleaned_data()
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1"
        )

        form = ProductForm(data, instance=self.product)
        form.is_valid()

    def test_product_price_assignments_based_on_product_variant_inline_formset_discounted_but_no_change_in_both_max_and_min_price_variant(
        self,
    ):
        """Tests that the prices for the instance of the
        :py:model:`~apps.products.models.product_models.Product`
        being created through the
        :py:meth:`apps.products.admin.ProductForm` have been assigned correctly.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&"
            # ProductVariant data (accessed through self.data)
            "productvariant_set-TOTAL_FORMS=5&"
            "productvariant_set-0-selling_price_0=2.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
            "productvariant_set-1-selling_price_0=5.30&"
            "productvariant_set-1-selling_price_1=ZAR&"
            "productvariant_set-2-selling_price_0=10.70&"
            "productvariant_set-2-selling_price_1=ZAR&"
            "productvariant_set-3-selling_price_0=4.20&"
            "productvariant_set-3-selling_price_1=ZAR&"
            "productvariant_set-4-selling_price_0=0.02&"
            "productvariant_set-4-selling_price_1=ZAR&"
            "productvariant_set-0-discounted_price_0=1.00&"
            "productvariant_set-0-discounted_price_1=ZAR&"
            "productvariant_set-2-discounted_price_0=9.70&"
            "productvariant_set-2-discounted_price_1=ZAR&"
            "productvariant_set-3-discounted_price_0=3.20&"
            "productvariant_set-3-discounted_price_1=ZAR&"
            "productvariant_set-4-discounted_price_0=0.01&"
            "productvariant_set-4-discounted_price_1=ZAR&"
        )

        form = ProductForm(data, instance=self.product)
        form.is_valid()

        assert form.instance.min_price.amount == Decimal(0.01).quantize(
            CURRENCY_PRECISION
        )
        assert form.instance.max_price.amount == Decimal(9.70).quantize(
            CURRENCY_PRECISION
        )
        assert form.instance.min_price_original.amount == Decimal(
            0.02
        ).quantize(CURRENCY_PRECISION)
        assert form.instance.max_price_original.amount == Decimal(
            10.70
        ).quantize(CURRENCY_PRECISION)

    def test_product_price_assignments_based_on_product_variant_inline_formset_discounted_with_changes_in_both_max_and_min_price_variant(
        self,
    ):
        """Tests that the prices for the instance of the
        :py:model:`~apps.products.models.product_models.Product`
        being created through the
        :py:meth:`apps.products.admin.ProductForm` have been assigned correctly.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&"
            # ProductVariant data (accessed through self.data)
            "productvariant_set-TOTAL_FORMS=5&"
            "productvariant_set-0-selling_price_0=2.00&"
            "productvariant_set-0-selling_price_1=ZAR&"
            "productvariant_set-1-selling_price_0=5.30&"
            "productvariant_set-1-selling_price_1=ZAR&"
            "productvariant_set-2-selling_price_0=10.70&"
            "productvariant_set-2-selling_price_1=ZAR&"
            "productvariant_set-3-selling_price_0=8.20&"
            "productvariant_set-3-selling_price_1=ZAR&"
            "productvariant_set-4-selling_price_0=3.02&"
            "productvariant_set-4-selling_price_1=ZAR&"
            "productvariant_set-0-discounted_price_0=1.89&"
            "productvariant_set-0-discounted_price_1=ZAR&"
            "productvariant_set-2-discounted_price_0=8.19&"
            "productvariant_set-2-discounted_price_1=ZAR&"
            "productvariant_set-4-discounted_price_0=0.01&"
            "productvariant_set-4-discounted_price_1=ZAR&"
        )

        form = ProductForm(data, instance=self.product)
        form.is_valid()

        assert form.instance.min_price.amount == Decimal(0.01).quantize(
            CURRENCY_PRECISION
        )
        assert form.instance.max_price.amount == Decimal(8.20).quantize(
            CURRENCY_PRECISION
        )
        assert form.instance.min_price_original.amount == Decimal(
            3.02
        ).quantize(CURRENCY_PRECISION)
        assert form.instance.max_price_original.amount == Decimal(
            8.20
        ).quantize(CURRENCY_PRECISION)

    def test_product_form_invalid_if_no_product_variant_data(
        self,
    ):
        """Tests that
        :py:meth:`~apps.products.admin.ProductForm`
        is invalid if no data for at least one
        :py:model:`~apps.products.models.product_models.ProductVariant`.

        Todo:
            *   Consider testing the error message as well using
                ``non_form_errors`` or by other means.
        """
        data = QueryDict(
            # Product data (accessed through self.cleaned_data())
            f"name={self.product.name}&sku_symbol={self.product.sku_symbol}&categories=1&option_types=1&option_types=2&option_types=3&"
            # ProductVariant data (accessed through self.data)
        )

        form = ProductForm(data, instance=self.product)
        assert not form.is_valid()


# ==============
# SkuAdmin Tests
# ==============
class TestSkuAdmin:
    """Tests for :py:class:`~apps.products.admin.SkuAdmin`."""

    # ------------------
    # Setup and Teardown
    # ------------------
    @pytest.fixture(autouse=True)
    def setup_test_db(self, db):
        """Sets up test database containing a basic
        :py:model:`~apps.products.models.product_models.Sku`
        object as well as ``AdminSite``.
        """
        SkuFactory()

        self.site = AdminSite()
        self.sku_admin = SkuAdmin(Sku, self.site)

    def test_add_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.SkuAdmin`
        add form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        assert list(self.sku_admin.get_form(request).base_fields) == [
            "sku_no",
            "product_variant_summary",
        ]
        assert list(self.sku_admin.get_fields(request)), [
            "sku_no",
            "product_variant_summary",
        ]

        # No excluded fields
        assert not self.sku_admin.get_exclude(request)

    def test_change_form_default_fields(self):
        """Tests that :py:class:`~apps.products.admin.SkuAdmin`
        change form has all expected fields and does not include fields
        which have been specifically excluded.
        """
        sku = Sku.objects.get(id=1)

        assert list(self.sku_admin.get_form(request, sku).base_fields) == [
            "sku_no",
            "product_variant_summary",
        ]
        assert list(self.sku_admin.get_fields(request, sku)) == [
            "sku_no",
            "product_variant_summary",
        ]

        # No excluded fields
        assert not self.sku_admin.get_exclude(request, sku)

    def test_correct_number_of_inlines(self):
        """Tests :py:class:`~apps.products.admin.SkuAdmin` has
        the expected number of inlines.
        """
        self.sku_admin = SkuAdmin(Sku, self.site)
        inline_instances = self.sku_admin.get_inline_instances(
            request, self.sku_admin
        )

        # No inlines
        assert len(inline_instances) == 0

    def test_sku_has_add_permission_is_false(self):
        """Tests that add permission for
        :py:class:`~apps.products.admin.SkuAdmin` is False."""

        sku_admin = SkuAdmin(Sku, self.site)

        assert not sku_admin.has_add_permission(request)

    def test_sku_has_change_permission_is_false(self):
        """Tests that change permission for
        :py:class:`~apps.products.admin.SkuAdmin` is False."""

        sku_admin = SkuAdmin(Sku, self.site)

        assert not sku_admin.has_change_permission(request)

    def test_sku_has_delete_permission_is_false(self):
        """Tests that delete permission for
        :py:class:`~apps.products.admin.SkuAdmin` is False."""
        sku_admin = SkuAdmin(Sku, self.site)

        assert not sku_admin.has_delete_permission(request)
