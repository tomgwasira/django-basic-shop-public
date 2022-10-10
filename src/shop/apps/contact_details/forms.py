#!/usr/bin/env python
"""Forms for Locations app."""

# Django library imports
from django.db.models import CharField, Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.forms.models import (
    ModelChoiceField,
    ModelForm,
    inlineformset_factory,
)

# Local application imports
from apps.users.models.user_profile_models import (
    GuestCustomerProfile,
    CustomerProfile,
    StaffProfile,
)
from .models.address_models import (
    GuestCustomerAddress,
    CustomerAddress,
)


__author__ = "Thomas Gwasira"
__date__ = "January 2022"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class CustomerAddressCreationForm(ModelForm):
    """Form for creation of
    :py:model:`~apps.users.models.address_models.CustomerAddress`.
    """

    class Meta:
        model = CustomerAddress
        exclude = ("customer_profile",)

    def __init__(self, *args, **kwargs):
        """Add the request to the form. This is necessary because it is required in the
        form's clean method."""
        self.request = kwargs.pop("request", None)
        super(CustomerAddressCreationForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Very important to set the customer_profile to which the address belongs
        before trying to save. Alternative would have been to create an inline formset; however, a
        bit of an overkill (which didn't work anyway) when all you need is
        just selection of a profile."""
        self.instance.customer_profile = self.request.user.customer_profile
        return super().clean()


class GuestCustomerAddressCreationForm(ModelForm):
    """Form for creation of
    :py:model:`~apps.users.models.address_models.GuestCustomerAddress`.
    """

    class Meta:
        model = CustomerAddress
        exclude = []

    def __init__(self, *arg, **kwarg):
        """Ensures inline formset created using this form cannot be left
        blank.
        """
        super(GuestCustomerAddressCreationForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


# Inline for creation of GuestCustomerAddress within GuestCustomerProfileCreationForm
GuestCustomerAddressCreationInlineFormset = inlineformset_factory(
    GuestCustomerProfile,
    GuestCustomerAddress,
    form=GuestCustomerAddressCreationForm,
    extra=1,
    can_delete=False,
    can_order=False,
)
