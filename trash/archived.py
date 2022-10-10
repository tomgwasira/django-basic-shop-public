# =================
# product_models.py
# =================
    def clean(self):
        """Validates
        :py:model:`~apps.products.product_models.ProductVariant` model.

        This method performs the following:
            1.   Checks that if both are specified, there is no conflict
                between the
                :py:attr:`~apps.products.product_models.ProductVariant.discounted_price`
                and the
                :py:attr:`~apps.products.product_models.ProductVariant.percentage_discount`
                attribute values.
            2.   Checks that
                :py:attr:`~apps.products.product_models.ProductVariant.discounted_price`
                is not greater or equal to
                :py:attr:`~apps.products.product_models.ProductVariant.selling_price`

        Raises:
            ValidationError: If there is a conflict between
                :py:attr:`~apps.products.product_models.ProductVariant.discounted_price`
                and
                :py:attr:`~apps.products.product_models.ProductVariant.percentage_discount`
            ValidationError: If
                :py:attr:`~apps.products.product_models.ProductVariant.discounted_price`
                is greater or equal to
                :py:attr:`~apps.products.product_models.ProductVariant.selling_price`

        Note:
            If
            :py:attr:`~apps.products.product_models.ProductVariant.discounted_price`
            is 0, it is considered to be blank.
        """
        # Check that, if specified, discounted price is not greater than
        # or equal to selling_price
        if getattr(self.discounted_price, "amount", None):
            if self.discounted_price.amount >= self.selling_price.amount:
                raise ValidationError(
                    "Discounted price cannot be greater or equal to"
                    + "selling price"
                )

    def save(self, *args, **kwargs):
        """Overrides the
        :py:model:`~apps.products.product_models.ProductVariant`
        ``save`` method to perform additional routines.

        This method performs the following:
            1.  Populates either
                :py:attr:`apps.products.product_models.ProductVariant.discounted_price`
                or
                :py:attr:`apps.products.product_models.ProductVariant.percentage_discount`
                if one of the attributes is blank while the other is not.
                The blank attribute is populated based on the value of
                the populated one.

        Warning:
            A
            :py:attr:`apps.products.product_models.ProductVariant.discounted_price`
            of value 0 is considered ``None``.
        """
        # Before use, first ensure that if there is no amount value
        # or if the discounted_price amount is 0, discounted_price
        # is considered None.
        if self.discounted_price:
            if not self.discounted_price.amount:
                self.discounted_price = None

        super(ProductVariant, self).save(*args, **kwargs)

    def get_price_with_multiple_items(self, item_quantity):
        # currency = self.selling_price.currency
        # print(currency)
        if self.discounted_price:
            total_price = self.discounted_price * item_quantity

        else:
            total_price = self.selling_price * item_quantity

        return total_price