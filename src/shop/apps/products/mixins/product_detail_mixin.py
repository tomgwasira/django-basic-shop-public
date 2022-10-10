"""Mixins for use on product detail page."""


class ProductDetailMixin:
    """Mixin to format data for a
    :py:model:`~apps.products.models.product_models.Product` such that it is in a
    form that is easier to use in front-end development."""

    def get_product_detail_extras(self, product):
        """Create nested collection of option types for given
        :py:model:`~apps.products.models.product_models.Product`.
        A collection of option values is specified for each option type where
        only the option values that have been added to the particular
        :py:model:`~apps.products.models.product_models.Product`'s
        :py:model:`~apps.products.models.product_models.ProductVariant`s are
        considered.

        To increase efficientcy, the logic for
        :py:func:`~apps.products.mixins.product_detail_mixin.ProductDetailMixin.get_simplified_product_variants`
        is also implemented here.

        Note:
            Structures of collections returned is meticulously selected and
            changes made should be effected in the front end frameworks as well

        Args:
            product (:py:model:`~apps.products.models.product_models.Product`):
                :py:model:`~apps.products.models.product_models.Product` object
                whose option types are to be obtained.

        Returns:
            (list, list): Tuple of list of dictionaries containing data about
                the relevant
                :py:model:`~apps.products.models.product_models.OptionType` and
                :py:model:`~apps.products.models.product_models.OptionValues`
                objects and list of
                :py:model:`~apps.products.models.product_models.ProductVariant`
                options information.
        """

        simplified_product_variants = []

        # Create dictionary of option types with option values nested in
        product_variants = product.product_variants.all()
        option_types = {}
        added_option_value_ids = (
            []
        )  # list to keep track of option values that have been added to
        # option_types to avoid duplicates

        for product_variant in product_variants:
            # Use dictionary of option types instead of array because want to extract option type using
            # key in front end
            simplified_product_variant = {"id": product_variant.id, "option_types": {}}
            # option_id_pairs = (
            #     {}
            # )  # information about an option value option type pairing to be
            # # added to simplified product variant

            option_values = product_variant.option_values.all()
            for option_value in option_values:
                simplified_product_variant["option_types"][option_value.option_type.id] = {"id": option_value.option_type.id, "name":option_value.option_type.name, "option_value": {"id": option_value.id, "name": option_value.name}}

                # Create option type - option value pairing for simplified
                # product variant
                # option_id_pairs[option_value.option_type.id] = option_value.id

                # Create option value dict object to be added to list of option
                # values for each option type
                option_value_data = {
                    "id": option_value.id,
                    "name": option_value.name,
                }

                # Create or update option type dict object to be added to list
                # of option types for the product
                if option_types.get(option_value.option_type.id):
                    # Check if option value dict has already been added to list
                    # of option values. If not, add it.
                    if option_value.id not in added_option_value_ids:
                        option_types[option_value.option_type.id][
                            "option_values"
                        ].append(option_value_data)
                        added_option_value_ids.append(option_value.id)
                else:
                    option_types[option_value.option_type.id] = {
                        "id": option_value.option_type.id,
                        "name": option_value.option_type.name,
                        "option_values": [option_value_data],
                    }
                    added_option_value_ids.append(option_value.id)

            simplified_product_variants.append(simplified_product_variant)
            # Add simplified product variant dict set up above to list of
            # simplified product variants
            # simplified_product_variants.append(
            #     {"id": product_variant.id, "option_id_pairs": option_id_pairs}
            # )

        return (list(option_types.values()), simplified_product_variants)
