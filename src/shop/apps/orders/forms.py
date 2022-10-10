#!/usr/bin/env python
"""Forms for Orders app."""

# Django library imports
from django.db.models import fields
from django.forms.fields import BooleanField
from django.forms.forms import Form
from django.forms.models import (
    ModelChoiceField,
    ModelForm,
    inlineformset_factory,
)

# Local application imports
from apps.users.models.user_models import RegisteredCustomerUser
from apps.contact_details.models.address_models import (
    CustomerAddress,
)

from .models.order_models import Order, OrderShippingMethod


__author__ = "Thomas Gwasira"
__date__ = "January 2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class OrderCreationForm(ModelForm):
    """Form for creation of
    :py:model:`~apps.orders.models.order_models.Order`.
    """

    # Add selection for shipping methods to the form
    shipping_method = ModelChoiceField(
        queryset=OrderShippingMethod.objects.all(), empty_label=None
    )

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
        )
