#!/usr/bin/env python
"""Admin classes and routines for *Products* app."""

# Django library
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import (
    BaseInlineFormSet,
    CheckboxSelectMultiple,
    ModelForm,
    Textarea,
    TextInput,
)
from django.utils import timezone
from django.utils.translation import gettext as _

# Third-party libraries
import nested_admin
from djmoney.money import Money
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

# Local application library
from shop import constants

from .models.image_models import *
from .models.note_models import *
from .models.product_models import *

__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


# =============
# CategoryAdmin
# =============
class CategoryHeroImageInline(admin.TabularInline):
    """Inline for
    :py:model:`~apps.products.models.image_models.CategoryHeroImage` on
    :py:class:`~apps.products.admin.CategoryAdmin` page.
    """

    model = CategoryHeroImage


class CategoryNoteInline(admin.TabularInline):
    """Inline for
    :py:model:`~apps.products.models.note_models.CategoryNote` on
    :py:class:`~apps.products.admin.CategoryAdmin` page.
    """

    model = CategoryNote

    def has_delete_permission(self, request, obj=None):
        """Removes ability to delete note inline.

        Note:
            Even though there will always be only one inline,
            there is a 'Delete' heading on the admin form and this
            method removes it.
        """
        return False


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    """Hierachical display for `django-treebeard`_ nested
    set :py:model:`~apps.products.models.product_models.Category`
    model.

    .. _django-treebeard: https://django-treebeard.readthedocs.io/en/latest/
    """

    form = movenodeform_factory(Category)

    inlines = (
        CategoryHeroImageInline,
        CategoryNoteInline,
    )


# ================
# OptionType Admin
# ================
class OptionValueOptionTypeInline(admin.TabularInline):
    """Inline for
    :py:model:`~apps.products.models.product_models.OptionValue` on
    :py:class:`~apps.products.admin.OptionTypeAdmin` page.
    """

    model = OptionValue


class OptionTypeNoteInline(admin.TabularInline):
    """Inline for
    :py:model:`~apps.products.models.note_models.OptionTypeNote` on
    :py:class:`~apps.products.admin.OptionTypeAdmin` page.
    """

    model = OptionTypeNote

    def has_delete_permission(self, request, obj=None):
        """Removes ability to delete note inline.

        Note:
            Even though there will always be only one inline,
            there is a 'Delete' heading on the admin form and this
            method removes it.
        """
        return False


@admin.register(OptionType)
class OptionTypeAdmin(admin.ModelAdmin):
    """Admin customisation for
    :py:model:`~apps.products.models.product_models.OptionType` model.

    Notes:
        Admin site actually labelled Options but named OptionType for more
        clarity on the main model.
    """

    inlines = (
        OptionValueOptionTypeInline,
        OptionTypeNoteInline,
    )


# ===============
# BrandAdmin Page
# ===============
class BrandNoteInline(admin.TabularInline):
    """Inline for
    :py:model:`~apps.products.models.note_models.BrandNote` on
    :py:class:`~apps.products.admin.BrandAdmin` page.
    """

    model = BrandNote

    def has_delete_permission(self, request, obj=None):
        """Removes ability to delete note inline.

        Note:
            Even though there will always be only one inline,
            there is a 'Delete' heading on the admin form and this
            method removes it.
        """
        return False


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin customisation for
    :py:model:`~apps.products.models.product_models.Brand` model.
    """

    inlines = (BrandNoteInline,)


# ==================
# SupplierAdmin Page
# ==================
class SupplierNoteInline(admin.TabularInline):
    """Inline for
    :py:model:`~apps.products.models.note_models.SupplierNote` on
    :py:class:`~apps.products.admin.SupplierAdmin` page.
    """

    model = SupplierNote

    def has_delete_permission(self, request, obj=None):
        """Removes ability to delete note inline.

        Note:
            Even though there will always be only one inline,
            there is a 'Delete' heading on the admin form and this
            method removes it.
        """
        return False


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Admin customisation for
    :py:model:`~apps.products.models.product_models.Supplier` model.
    """

    inlines = (SupplierNoteInline,)


# =================
# ProductAdmin Page
# =================
class OptionValueProductVariantInlineFormSet(BaseInlineFormSet):
    """Inline formset for
    :py:class:`~apps.products.admin.OptionValueProductVariantInline`.

    Comment:
        The formset is required to override the clean method which
        cannot be done using just an inline.
    """

    def clean(self):
        """Validates and performs additional routines using data from
        :py:class:`~apps.products.admin.OptionValueProductVariantInlineFormSet`

        This method performs the following:
            1.  Checks that there is exactly one
                :py:model:`~apps.products.models.product_models.OptionValue`
                for each
                :py:model:`~apps.products.models.product_models.OptionType`.

            2.  Checks that there are no additional
                :py:model:`~apps.products.models.product_models.OptionValue`s
                specified beyond
                :py:model:`~apps.products.models.product_models.OptionTypes`s
                specified for the related
                :py:model:`~apps.products.models.product_models.Product`.

            3.  Generates the
                :py:attr:`~apps.products.models.product_models.ProductVariant.sku_no`.

            4.  Generates the
                :py:attr:`~apps.products.models.product_models.ProductVariant.product_variant_summary`.

            5.  Sets the
                :py:attr:`~apps.products.models.product_models.ProductVariant.is_form_validated`
                flag.

        Raises:
            ValidationError: If there is less or more than oneone
                :py:model:`~apps.products.models.product_models.OptionValue`
                for each
                :py:model:`~apps.products.models.product_models.OptionType`.
            ValidationError: If there are additional
                :py:model:`~apps.products.models.product_models.OptionValue`s
                specified beyond
                :py:model:`~apps.products.models.product_models.OptionTypes`s
                specified for the related
                :py:model:`~apps.products.models.product_models.Product`.

        Note:
            Most of the routines carried out here require use of data from the m2m
            field
            :py:attr:`~apps.products.models.product_models.ProductVariant.option_values`.
            This is why they were not performed in the ``clean`` or
            ``save`` methods of the
            :py:model:`~apps.products.models.product_models.ProductVariant`
            model as the m2m data would have disappeared by then.
            An alternative would have been to use the ``m2m_changed``
            signal. However, this would have to be called post-save which
            is not useful because the intention is to prevent saving the
            object if anything is wrong.
        """
        super(OptionValueProductVariantInlineFormSet, self).clean()

        if self.is_valid():
            # -----------------------------------------
            # OptionValue-OptionType Pairing Validation
            # -----------------------------------------
            # Check that there is exactly one OptionValue for each OptionType
            # of the related Product
            option_type_ids = []
            for option_value_formset_item in self.cleaned_data:
                if option_value_formset_item:
                    option_type_ids.append(
                        # Convert to string because option_type data from form
                        # is list of strings
                        str(
                            option_value_formset_item[
                                "optionvalue"
                            ].option_type.id
                        )
                    )

            product_option_type_ids = self.data.getlist("option_types")

            missing_option_types = []
            duplicated_option_types = []
            for product_opt_typ_id in product_option_type_ids:
                n_opt_typ_occurrences = option_type_ids.count(
                    product_opt_typ_id
                )

                if n_opt_typ_occurrences < 1:
                    missing_option_types.append(
                        OptionType.objects.get(id=int(product_opt_typ_id)).name
                    )

                elif n_opt_typ_occurrences > 1:
                    duplicated_option_types.append(
                        OptionType.objects.get(id=int(product_opt_typ_id)).name
                    )

            missing_option_types_str = (
                ""  # display string for when there are missing option_types
            )
            duplicated_option_types_str = (
                ""  # display string for when there are duplicated option_types
            )

            # Create string to be used for ValidationError for missing option_types
            if len(missing_option_types) == 1:
                missing_option_types_str = missing_option_types[0]

            elif len(missing_option_types) > 1:
                for i in range(len(missing_option_types) - 1):
                    missing_option_types_str += missing_option_types[i] + ", "
                missing_option_types_str = (
                    missing_option_types_str[:-2]
                    + " and "
                    + missing_option_types[-1]
                )

            # Create string to be used for ValidationError for duplicated option_types
            if len(duplicated_option_types) == 1:
                duplicated_option_types_str = duplicated_option_types[0]

            elif len(duplicated_option_types) > 1:
                for i in range(len(duplicated_option_types) - 1):
                    duplicated_option_types_str += (
                        duplicated_option_types[i] + ", "
                    )
                duplicated_option_types_str = (
                    duplicated_option_types_str[:-2]
                    + " and "
                    + duplicated_option_types[-1]
                )

            # Raise ValidationErrors
            if (
                len(missing_option_types) > 0
                and len(duplicated_option_types) == 0
            ):
                raise ValidationError(
                    _(
                        "Ensure that you have specified the %(missing_option_types_str)s."
                    ),
                    code="invalid",
                    params={
                        "missing_option_types_str": missing_option_types_str
                    },
                )

            elif (
                len(duplicated_option_types) > 0
                and len(missing_option_types) == 0
            ):
                raise ValidationError(
                    _(
                        "Cannot have more than one value for %(duplicated_option_types_str)s."
                    ),
                    code="invalid",
                    params={
                        "duplicated_option_types_str": duplicated_option_types_str
                    },
                )

            elif (
                len(missing_option_types) > 0
                and len(duplicated_option_types) > 0
            ):
                raise ValidationError(
                    [
                        ValidationError(
                            _(
                                "Ensure that you have specified the %(missing_option_types_str)s."
                            ),
                            code="invalid",
                            params={
                                "missing_option_types_str": missing_option_types_str
                            },
                        ),
                        ValidationError(
                            _(
                                "Cannot have more than one value for %(duplicated_option_types_str)s."
                            ),
                            code="invalid",
                            params={
                                "duplicated_option_types_str": duplicated_option_types_str
                            },
                        ),
                    ]
                )

            # Check that there are no additional OptionValues specified beyond
            # the OptionTypes specified for the related Product
            for option_type_id in option_type_ids:
                n_opt_typ_occurrences = product_option_type_ids.count(
                    option_type_id
                )

                if n_opt_typ_occurrences < 1:
                    raise ValidationError(
                        _("Product does not have %(option_type)s attribute."),
                        code="invalid",
                        params={
                            "option_type": OptionType.objects.get(
                                id=int(option_type_id)
                            ).name
                        },
                    )

            # -------------------
            # SKU Code Generation
            # -------------------
            sku_no = self.instance.product.sku_symbol

            for option_value_formset_item in self.cleaned_data:
                if option_value_formset_item:
                    sku_no += (
                        "-"
                        + option_value_formset_item["optionvalue"].sku_symbol
                    )

            self.instance.sku_no = sku_no.strip()

            # Check if SKU number exists and if so, make current one unique
            if ProductVariant.objects.filter(sku_no=self.instance.sku_no):
                count = 2  # starting from 2 since there is already one SKU with the desired code
                while True:
                    if not ProductVariant.objects.filter(
                        sku_no=self.instance.sku_no + "-" + str(count)
                    ):
                        self.instance.sku_no = (
                            self.instance.sku_no + "-" + str(count)
                        )
                        break
                    else:
                        count += 1

            # ---------------------------------
            # ProductVariant Summary Generation
            # ---------------------------------
            categories = []

            for category_id in self.data.getlist("categories"):
                categories.append(Category.objects.get(id=category_id).name)

            option_values = []
            for option_value_formset_item in self.cleaned_data:
                if (
                    option_value_formset_item
                ):  # some formsets may be empty esp. when extras are used
                    option_values.append(
                        option_value_formset_item["optionvalue"].name
                    )

            self.instance.product_variant_summary = {
                "sku_no": self.instance.sku_no,
                "name": self.instance.product.name,
                "categories": categories,
                "option_values": option_values,
                "created_at": timezone.now().strftime("%c"),
            }

            # --------------------------
            # Set is_form_validated Flag
            # --------------------------
            self.is_form_validated = True


class OptionValueProductVariantInline(nested_admin.NestedStackedInline):
    """Inline for
    :py:model:`~apps.products.models.product_models.OptionValue` on
    :py:class:`~apps.products.admin.ProductVariantInline` which in turn
    is an inline on :py:class:`~apps.products.admin.ProductAdmin` page
    (i.e. nested inline).

    Uses the through model which results in there being only dropdowns
    of
    :py:model:`~apps.products.models.product_models.OptionValue` whereby
    only one can be selected per dropdown rather than an m2m widget.
    """

    model = ProductVariant.option_values.through
    formset = OptionValueProductVariantInlineFormSet
    extra = 0


# class ProductVariantImageInline(nested_admin.NestedTabularInline):
#     """Inline for
#     :py:model:`~apps.products.models.product_models.ProductVariantImage` on
#     :py:class:`~apps.products.admin.ProductVariantInline` which in turn
#     is an inline on :py:class:`~apps.products.admin.ProductAdmin` page
#     (i.e. nested inline).
#     """

#     model = ProductVariantImage


class ProductVariantInline(nested_admin.NestedTabularInline):
    """Inline for
    :py:model:`~apps.products.models.product_models.ProductVariant` on
    :py:class:`~apps.products.admin.ProductAdmin` page.
    """

    model = ProductVariant
    min_num = 1  # there should always be one ProductVariant even when no OptionTypes are specified for the Product
    extra = 0

    inlines = (
        OptionValueProductVariantInline,
        # ProductVariantImageInline,
    )

    exclude = (
        "sku_no",
        "product_variant_summary",
        "is_form_validated",
        "option_values",
    )


class ProductImageInline(nested_admin.NestedTabularInline):
    """Inline for
    :py:model:`~apps.products.models.image_models.ProductImage` on
    :py:class:`~apps.products.admin.ProductAdmin` page.
    """

    model = ProductImage
    extra = 0


class ProductThumbnailImageInline(nested_admin.NestedTabularInline):
    """Inline for
    :py:model:`~apps.products.models.image_models.ProductImage` on
    :py:class:`~apps.products.admin.ProductAdmin` page.
    """

    model = ProductThumbnailImage
    extra = 0


class TagInline(nested_admin.NestedTabularInline):
    """Inline for
    :py:model:`~apps.products.models.product_models.Tag` on
    :py:class:`~apps.products.admin.ProductAdmin` page.
    """

    model = Tag


class ProductNoteInline(nested_admin.NestedTabularInline):
    """Inline for
    :py:model:`~apps.products.models.note_models.ProductNote` on
    :py:class:`~apps.products.admin.ProductAdmin` page.
    """

    model = ProductNote

    def has_delete_permission(self, request, obj=None):
        """Removes ability to delete note inline.

        Note:
            Even though there will always be only one inline,
            there is a 'Delete' heading on the admin form and this
            method removes it.
        """
        return False


class ProductForm(ModelForm):
    """Form for :py:class:`~apps.products.admin.Product`.

    Comment:
        The formset is required to override the clean method which
        cannot be done using just a ``ModelAdmin``.
    """

    class Meta:
        model = Product
        exclude = (
            "min_price",
            "max_price",
            "min_price_original",
            "max_price_original",
            "is_form_validated",
        )

    def clean(self):
        """Validates and performs additional routines using data from
        :py:class:`~apps.products.admin.ProductForm`.

        This method does the following:
            1.  Checks that if a child
                :py:model:`~apps.products.models.product_models.Category`
                is added to the
                :py:model:`~apps.products.models.product_models.Product`
                then its parent is not also being added.

            2.  Checks that user is not attempting to create duplicate
                :py:model:`~apps.products.models.product_models.ProductVariant`
                objects. One of the two attributes:
                :py:attr:`~apps.products.models.product_models.ProductVariant.option_values`,
                or
                :py:attr:`~apps.products.models.product_models.ProductVariant.supplier`,
                needs to be different. Not allowing different prices without different
                :py:attr:`~apps.products.models.product_models.ProductVariant.option_values`
                or
                :py:attr:`~apps.products.models.product_models.ProductVariant.supplier`,
                because it then becomes difficult for user to keep track of which
                :py:model:`~apps.products.models.product_models.ProductVariant` is
                which based on just prices.

            3.  Goes through the
                :py:class:`~apps.products.admin.ProductVariantInlineFormset.`
                data values of
                :py:attr:`~apps.products.models.product_models.ProductVariant.selling_price`
                and
                :py:attr:`~apps.products.models.product_models.ProductVariant.discounted_price`,
                finds the minimum and maximum out of these and sets the
                :py:attr:`~apps.products.models.product_models.Product.min_price`,
                :py:attr:`~apps.products.models.product_models.Product.max_price`,
                :py:attr:`~apps.products.models.product_models.Product.min_price_original`,
                and
                :py:attr:`~apps.products.models.product_models.Product.max_price_original`,
                attributes of the the current
                :py:model:`~apps.products.models.product_models.Product`
                Product instance.

            4.  Sets the
                :py:attr:`~apps.products.models.product_models.Product.is_form_validated`
                flag.

        Raises:
            ValidationError: If both a child and a parent
                :py:model:`~apps.products.models.product_models.Category`
                are being added to the
                :py:model:`~apps.products.models.product_models.Product`.
            ValidationError: If user is attempting to create multiple
                :py:model:`~apps.products.models.product_models.ProductVariant`s
                with identical
                :py:model:`~apps.products.models.product_models.OptionValue`s
                and :py:model:`~apps.products.models.product_models.Supplier`,
                thereby duplicating the
                :py:model:`~apps.products.models.product_models.ProductVariant`.
            ValidationError: If
                :py:class:`~apps.products.admin.ProductVariantInlineFormset.`
                does not have ``selling_price`` values such that
                :py:attr:`~apps.products.models.product_models.Product.min_price`
                and
                :py:attr:`~apps.products.models.product_models.Product.max_price`,
                cannot be populated. This, however, is unlikely to happen as
                :py:attr:`~apps.products.models.product_models.ProductVariant.selling_price`,
                is set to not be blank.
            ValidationError: If user is attempting to create a
                :py:model:`~apps.products.models.product_models.Product`
                without at least one
                :py:model:`~apps.products.models.product_models.ProductVariant`.
                This, however, is unlikely to happen as the form is set
                to always have a minimum of one
                :py:class:`~apps.products.admin.ProductVariantInlineFormset`.
        """

        super(ProductForm, self).clean()

        if self.is_valid():
            # ----------------------------
            # Category Branches Validation
            # ----------------------------
            # Create list of strings representing branches of Categories
            # for ProductVariant
            category_branches = []

            # Empty list if none.
            # Deliberately throws error if "categories" doesn't exist.
            for category in self.cleaned_data["categories"]:
                # Make string to represent branch of Categories
                # Using strings as they are more efficient than lists
                category_branch = ""
                for ancestor_category in Category.objects.get(
                    id=category.id
                ).get_ancestors():
                    category_branch += ancestor_category.name + ", "
                category_branch += category.name

                category_branches.append(category_branch)

            # Ensure if a child Category is added, then parent Category
            # is not also added
            for category_branch_i in category_branches:
                for category_branch_j in category_branches:
                    # Check if one added category_branch is substring of another
                    if (
                        category_branch_i in category_branch_j
                        and category_branch_i != category_branch_j
                    ):
                        raise ValidationError(
                            _(
                                "Cannot set both '%(category_i)s' and '%(category_j)s' as the product's categories."
                            ),
                            code="invalid",
                            params={
                                "category_i": category_branch_i.split(",")[
                                    -1
                                ].strip(),
                                "category_j": category_branch_j.split(",")[
                                    -1
                                ].strip(),
                            },
                        )

            # ------------------------------
            # ProductVariant Data Extraction
            # ------------------------------
            product_variants_data = []
            currencies = []
            original_prices = []
            actual_prices = []
            # Check if at least one ProductVariant is specified
            # Because TOTAL_FORMS is a string, will need to be converted
            # to int otherwise "0" will evaluate to True.

            if self.data.get("product_variants-TOTAL_FORMS") and int(
                self.data["product_variants-TOTAL_FORMS"]
            ):
                # Iterate over ProductVariants
                for i in range(int(self.data["product_variants-TOTAL_FORMS"])):
                    product_variant_data = {}
                    # ~~~~~~~~~~~~~~~~
                    # OptionValue Data
                    # ~~~~~~~~~~~~~~~~
                    option_value_ids = []
                    # Check if at least one OptionValue is specified
                    # Because TOTAL_FORMS is a string, will need to be converted
                    # to int otherwise "0" will evaluate to True
                    if self.data.get(
                        f"product_variants-{str(i)}-ProductVariant_option_values-TOTAL_FORMS"
                    ) and int(
                        self.data[
                            f"product_variants-{str(i)}-ProductVariant_option_values-TOTAL_FORMS"
                        ]
                    ):
                        # Iterate over OptionValues
                        for j in range(
                            int(
                                self.data[
                                    f"product_variants-{str(i)}-ProductVariant_option_values-TOTAL_FORMS"
                                ]
                            )
                        ):
                            if self.data.get(
                                f"product_variants-{str(i)}-ProductVariant_option_values-{str(j)}-optionvalue"
                            ):
                                option_value_ids.append(
                                    int(
                                        self.data[
                                            f"product_variants-{str(i)}-ProductVariant_option_values-{str(j)}-optionvalue"
                                        ]
                                    )
                                )

                        option_value_ids.sort()

                        # Sorted list of ids of all OptionValues for current ProductVariant
                        product_variant_data[
                            "sorted_option_value_ids"
                        ] = option_value_ids

                    # ~~~~~~~~~~~~~
                    # Supplier Data
                    # ~~~~~~~~~~~~~
                    # Nonetype is acceptable
                    product_variant_data["supplier_id"] = self.data.get(
                        f"product_variants-{str(i)}-ProductVariant_supplier"
                    )

                    product_variants_data.append(product_variant_data)

                    # ~~~~~~~~~~
                    # Price Data
                    # ~~~~~~~~~~
                    if self.data.get(
                        f"product_variants-{str(i)}-selling_price_0"
                    ) and not self.data.get(
                        f"product_variants-{str(i)}-discounted_price_0"
                    ):
                        # Not checking whether this exists for better performance.
                        # Would rather have it throw error as it is very unlikely that
                        # selling_price_0 would exist and not selling_price_1. Same
                        # argument for the rest of the code applies.
                        currencies.append(
                            self.data[
                                f"product_variants-{str(i)}-selling_price_1"
                            ]
                        )

                        original_prices.append(
                            Decimal(
                                eval(
                                    self.data[
                                        f"product_variants-{str(i)}-selling_price_0"
                                    ]
                                )
                            ).quantize(constants.CURRENCY_PRECISION)
                        )
                        actual_prices.append(
                            Decimal(
                                eval(
                                    self.data[
                                        f"product_variants-{str(i)}-selling_price_0"
                                    ]
                                )
                            ).quantize(constants.CURRENCY_PRECISION)
                        )

                    # If discounted_price specified, take it as actual price and
                    # selling_price as original price
                    elif self.data.get(
                        f"product_variants-{str(i)}-selling_price_0"
                    ) and self.data.get(
                        f"product_variants-{str(i)}-discounted_price_0"
                    ):
                        original_prices.append(
                            Decimal(
                                eval(
                                    self.data[
                                        f"product_variants-{str(i)}-selling_price_0"
                                    ]
                                )
                            ).quantize(constants.CURRENCY_PRECISION)
                        )
                        currencies.append(
                            self.data[
                                f"product_variants-{str(i)}-discounted_price_1"
                            ]
                        )
                        actual_prices.append(
                            Decimal(
                                eval(
                                    self.data[
                                        f"product_variants-{str(i)}-discounted_price_0"
                                    ]
                                )
                            ).quantize(constants.CURRENCY_PRECISION)
                        )

                    # Raise ValidationError if selling_price not specified
                    else:
                        raise ValidationError(
                            _(
                                "Product variant selling prices cannot be blank."
                            ),
                            code="invalid",
                        )

                # ---------------------
                # Currencies Validation
                # ---------------------
                # Raise ValidationError if different currencies used
                if len(currencies) > 0:
                    for currency in currencies:
                        if currency != currencies[0]:
                            raise ValidationError(
                                _(
                                    "Cannot use more than one currency at a time."
                                ),
                                code="invalid",
                            )

                    # ----------------
                    # Price Population
                    # ----------------
                    # Populate prices for Product
                    currency = currencies[0]

                    self.instance.min_price = Money(
                        min(actual_prices), currency
                    )
                    # self.instance.min_price = Money(10, currency)
                    self.instance.max_price = Money(
                        max(actual_prices), currency
                    )
                    self.instance.min_price_original = Money(
                        original_prices[
                            actual_prices.index(self.instance.min_price.amount)
                        ],
                        currency,
                    )
                    self.instance.max_price_original = Money(
                        original_prices[
                            actual_prices.index(self.instance.max_price.amount)
                        ],
                        currency,
                    )

                # -------------------------------------
                # ProductVariant Duplication Validation
                # -------------------------------------
                # Raise ValidationError if at two or more ProductVariants have identical
                # set of OptionValues and same Supplier as well
                for i in range(len(product_variants_data)):
                    for j in range(len(product_variants_data)):
                        if (
                            # Don't compare an element with itself
                            i != j
                            and product_variants_data[i].get(
                                "sorted_option_value_ids"
                            )
                            == product_variants_data[j].get(
                                "sorted_option_value_ids"
                            )
                            and product_variants_data[i].get("supplier_id")
                            == product_variants_data[j].get("supplier_id")
                        ):
                            raise ValidationError(
                                _(
                                    "Two product variants cannot have identical set of option values and the same supplier"
                                ),
                                code="invalid",
                            )

            # --------------------------------------
            # No ProductVariant Specified Validation
            # --------------------------------------
            # Raise ValidationError if user trying to create Product without ProductVariant
            else:
                raise ValidationError(
                    _("At least one product variant should be created."),
                    code="invalid",
                )

            self.instance.is_form_validated = True


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    """Admin customisation for
    :py:model:`~apps.products.models.product_models.Product` model.

    M2m field for
    :py:model:`~apps.products.models.product_models.OptionType`
    is overriden to use checkbox widget.
    """

    # change_form_template = 'admin/product_admin.html'

    form = ProductForm

    inlines = (
        ProductImageInline,
        ProductThumbnailImageInline,
        # TagInline,
        ProductNoteInline,
        ProductVariantInline,
    )

    # exclude = (
    #             'min_price',
    #             'max_price'
    #           )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """Uses checkbox widget for
        :py:model:`~apps.products.models.product_models.OptionType` m2m
        formfield.
        """
        if db_field.name == "option_types":
            kwargs["widget"] = CheckboxSelectMultiple()
            kwargs[
                "help_text"
            ] = ""  # TODO: Consider adding some help text here

        return db_field.formfield(**kwargs)


# # =========
# # Sku Admin
# # =========
# @admin.register(Sku)
# class SkuAdmin(admin.ModelAdmin):
#     """Admin customisation for
#     :py:model:`~apps.products.models.product_models.Sku` model.
#     """

#     def has_add_permission(self, request, obj=None):
#         """Removes ability to add an
#         :py:model:`~apps.products.models.product_models.Sku` object
#         using admin form

#         New Sku objects can only be created_at when saving a
#         :py:model:`~apps.products.models.product_models.ProductVariant`.
#         """
#         return False

#     def has_change_permission(self, request, obj=None):
#         """Removes ability to modify an
#         :py:model:`~apps.products.models.product_models.Sku` object.
#         using admin form.
#         """
#         return False

#     def has_delete_permission(self, request, obj=None):
#         """Removes ability to delete an
#         :py:model:`~apps.products.models.product_models.Sku` object.
#         """
#         return False
