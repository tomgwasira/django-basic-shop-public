"""Mixins for validations during creation of objects for models in Products
app.
"""
from decimal import Decimal
from apps.products.models.product_models import (
    Category,
    OptionValue,
    OptionType,
    ProductVariant,
)
from django.shortcuts import get_object_or_404
from shop import constants
from djmoney.money import Money

__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class ProductAdminMixin:
    """Mixins for routines during creation or update of
    :py:model:`~apps.products.models.product_models.Product` objects.
    """

    def _validate_category_branches(self, categories):
        """Check that, given a list of
        :py:model:`~apps.products.models.product_models.Category` primary keys,
        if a child :py:model:`~apps.products.models.product_models.Category`
        is in the list, then the parent is also not included in the list.

        Args:
            category_pks (list): List of primary keys for the
                :py:model:`~apps.products.models.product_models.Category`
                objects to be added to the
                :py:model:`~apps.products.models.product_models.Product`
                object.
        """
        category_pks = [i.pk for i in categories]

        category_branches = (
            []
        )  # list of tuples representing branches of Categories for Product

        for category_pk in category_pks:
            # Use string because easiest to check if one string is a substring
            # of another
            category_branch = ""

            # Build string representing branch from root to current Category
            # as leaf
            for ancestor_category in get_object_or_404(
                Category, pk=category_pk
            ).get_ancestors():
                category_branch += str(ancestor_category.pk) + ", "
            category_branch += str(category_pk)

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
                    category_name_i = get_object_or_404(
                        Category, pk=category_branch_i.split(",")[-1].strip()
                    ).name
                    category_name_j = get_object_or_404(
                        Category, pk=category_branch_j.split(",")[-1].strip()
                    )
                    return (
                        False,
                        f"Cannot set both '{category_name_i}' and "
                        + f"'{category_name_j}' as the product's categories. "
                        + "Ensure that if a child category is added, then the "
                        + "parent has not also been added.",
                    )

        return (True, None)

    def _validate_product_and_populate_fields(self, product_data):
        """The routines have been bundled up in this manner to avoid having to
        iterate through a list of product variants multiple times.

        This method does the following:

        Check that given a list of lists of
        :py:model:`~apps.products.models.product_models.OptionValue` primary
        keys, corresponding to each
        :py:model:`~apps.products.models.product_models.ProductVariant` of the
        current :py:model:`~apps.products.models.product_models.Product`, each
        list contains a unique, order insensitive, combination  of primary
        keys.

        This implies that no
        :py:model:`~apps.products.models.product_models.ProductVariant` has
        been duplicated.
        """
        # ------------------------------------------------
        # At Least One ProductVariant Specified Validation
        # ------------------------------------------------
        if not product_data["product_variants"]:
            return (False, "At least one product variant must be specified.")

        all_option_value_pks = []

        currency = ""
        original_prices = []
        actual_prices = []

        for product_variant_data in product_data["product_variants"]:
            # Initialise currency with value of first ProductVariant's selling_price_currency
            currency = product_variant_data["selling_price"].currency

            # -------------------------------------
            # ProductVariant Duplication Validation
            # -------------------------------------
            # Iterate over data supplied for creation of a ProductVariant. Make a
            # list of sorted OptionValue pk's for creation of the ProductVariant
            # and if the same combination of OptionValue pk's has been encountered
            # before, return.

            # Use list because need to sort option value pks before checking if
            # duplicated
            option_value_pks = []
            for option_value in product_variant_data["option_values"]:
                option_value_pks.append(option_value.pk)
            option_value_pks.sort()
            if option_value_pks not in all_option_value_pks:
                all_option_value_pks.append(option_value_pks)
            else:
                # Build string of duplicated OptionValue names to be used in
                # error message and return error if two ProductVariants with
                # identical OptionValue combinations
                option_value_names = ""

                if len(option_value_pks) > 1:
                    for i in range(len(option_value_pks) - 1):
                        option_value_names += (
                            "'"
                            + get_object_or_404(
                                OptionValue, pk=option_value_pks[i]
                            ).name
                            + "', "
                        )
                    last_option_value_name = get_object_or_404(
                        OptionValue, pk=option_value_pks[-1]
                    ).name
                    option_value_names = (
                        option_value_names[:-2]
                        + f" and '{last_option_value_name}'"
                    )

                    return (
                        False,
                        (
                            "Product variant with option values"
                            + f" {option_value_names} duplicated.",
                        ),
                    )

                else:
                    option_value_names += get_object_or_404(
                        OptionValue, pk=option_value_pks[0]
                    ).name

                    return (
                        False,
                        (
                            "Product variant with option value"
                            + f" '{option_value_names}' duplicated.",
                        ),
                    )

            # ------------------------------------
            # Price Data Extraction and Validation
            # ------------------------------------
            if (
                product_variant_data["selling_price"]
                and not product_variant_data["discounted_price"]
            ):
                if product_variant_data["selling_price"].currency != currency:
                    return (
                        False,
                        "Cannot use more than one currency at a time.",
                    )

                original_prices.append(
                    product_variant_data["selling_price"].amount
                )

                actual_prices.append(
                    product_variant_data["selling_price"].amount
                )

            elif (
                product_variant_data["selling_price"]
                and product_variant_data["discounted_price"]
            ):
                if product_variant_data["selling_price"].currency != currency:
                    return (
                        False,
                        "Cannot use more than one currency at a time.",
                    )

                if (
                    product_variant_data["discounted_price"].currency
                    != currency
                ):
                    return (
                        False,
                        "Cannot use more than one currency at a time.",
                    )

                original_prices.append(
                    product_variant_data["selling_price"].amount
                )

                actual_prices.append(
                    product_variant_data["discounted_price"].amount
                )

            else:
                return (
                    False,
                    "Product variant selling prices cannot be blank.",
                )

        # Add values for price range to product data
        product_data["min_price"] = Money(min(actual_prices), currency)
        product_data["max_price"] = Money(max(actual_prices), currency)
        product_data["min_price_original"] = Money(
            original_prices[
                actual_prices.index(product_data["min_price"].amount)
            ],
            currency,
        )
        product_data["max_price_original"] = Money(
            original_prices[
                actual_prices.index(product_data["max_price"].amount)
            ],
            currency,
        )

        return (True, None)


class ProductVariantAdminMixin:
    def _validate_option_type_option_value_pairings(
        self, option_values, product_option_type_pks
    ):
        """"""
        error_messages = []

        # Check that there is exactly one OptionValue for each OptionType
        # required by the Product
        product_variant_option_type_pks = []

        for option_value in option_values:
            product_variant_option_type_pks.append(option_value.option_type.pk)

        missing_option_type_names = []
        duplicated_option_type_names = []

        for product_option_type_pk in product_option_type_pks:
            n_option_type_occurrences = product_variant_option_type_pks.count(
                product_option_type_pk
            )

            if n_option_type_occurrences < 1:
                missing_option_type_names.append(
                    get_object_or_404(
                        OptionType, pk=product_option_type_pk
                    ).name
                )

            elif n_option_type_occurrences > 1:
                duplicated_option_type_names.append(
                    get_object_or_404(
                        OptionType, pk=product_option_type_pk
                    ).name
                )

        # Check that ProductVariant doesn't have any extra OptionTypes
        # (OptionValues) not required by Product
        for product_variant_option_type_pk in product_variant_option_type_pks:
            if (
                product_option_type_pks.count(product_variant_option_type_pk)
                < 1
            ):
                error_messages.append(
                    "Product does not have option type '"
                    + f"{get_object_or_404(OptionType, pk=product_variant_option_type_pk).name}'"
                )

        # Create error messages for missing OptionTypes
        if len(missing_option_type_names) == 1:
            error_messages.append(
                "Ensure you have specified an option value for '"
                + f"{missing_option_type_names[0]}'."
            )

        elif len(missing_option_type_names) > 1:
            missing_option_type_names_str = ""
            for missing_option_type_name in range(
                len(missing_option_type_names) - 1
            ):
                missing_option_type_names_str += (
                    "'" + missing_option_type_name + "', "
                )
            missing_option_type_names = missing_option_type_names[:-2] + (
                f" and '{missing_option_type_names[-1]}'"
            )

            error_messages.append(
                "Ensure you have specified option values for "
                + f"{missing_option_type_names_str}."
            )

        # Create error messages for duplicated OptionTypes
        if len(duplicated_option_type_names) == 1:
            error_messages.append(
                "Cannot have more than one option value for '"
                + f"{duplicated_option_type_names[0]}'."
            )

        elif len(duplicated_option_type_names) > 1:
            duplicated_option_type_names_str = ""
            for duplicated_option_type_name in range(
                len(duplicated_option_type_names) - 1
            ):
                duplicated_option_type_names_str += (
                    "'" + duplicated_option_type_name + "', "
                )
            duplicated_option_type_names = duplicated_option_type_names[
                :-2
            ] + (f" and '{duplicated_option_type_names[-1]}'")

            error_messages.append(
                "Cannot have more than one option value for '"
                + f"{duplicated_option_type_names_str}'."
            )

        if len(error_messages) > 0:
            return (False, error_messages)

        return (True, None)

    def generate_sku_no(self, data):
        """Algorithm for generation of SKU number.

        This could have been incorporated in the whole validation for ProductVariant. However, because this algorithm may change, for scalability,
        this has been implemented separately albeit, causing additional computation time to iterate over the OptionValues."""
        sku_no = ""

        for option_value in data["option_values"]:
            sku_no += option_value.sku_symbol

        counter = 1
        while True:
            if not ProductVariant.objects.filter(
                sku_no=sku_no + "-" + str(counter)
            ).count():
                break
            else:
                counter += 1

        if counter == 1:
            return sku_no

        return sku_no + "-" + str(counter)
