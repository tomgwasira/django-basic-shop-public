#!/usr/bin/env python
"""Forms for Users app.

Only forms and formsets required in views (and not admin) are defined
here. Any forms and formsets related to the admin are defined in the
:py:mod:`~apps.users.admin` module. However, forms defined here are also
used in :py:mod:`~apps.users.admin`.
"""

# Django library imports
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
    UserChangeForm,
)
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import HiddenInput


# Local application imports
from .models.user_models import GuestCustomerUser, RegisteredCustomerUser
from apps.users.models.user_profile_models import (
    GuestCustomerProfile,
    CustomerProfile,
)


__author__ = "Thomas Gwasira"
__date__ = "December 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


# =========================
# Registered Customer Forms
# =========================
class RegisteredCustomerUserCreationForm(UserCreationForm):
    """Form for creation of a
    :py:model:`~apps.users.models.user_models.RegisteredCustomerUser`.

    The proxy model
    :py:model:`~apps.users.models.user_models.RegisteredCustomerUser`
    is used here rather than the
    :py:model:`~apps.users.models.user_models.BaseUser` model such that
    on saving the form, the
    :py:meth:`~apps.users.models.user_models.RegisteredCustomerUser.save`
    method of the proxy is called.
    """

    class Meta:
        model = RegisteredCustomerUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        """Constructor for form.

        This removes help text from specified fields.
        """
        super(RegisteredCustomerUserCreationForm, self).__init__(
            *args, **kwargs
        )

        for fieldname in ["password1", "password2"]:
            self.fields[fieldname].help_text = None


class RegisteredCustomerUserChangeForm(UserChangeForm):
    """Form for changing of a
    :py:model:`~apps.users.models.user_models.RegisteredCustomerUser`.

    The proxy model
    :py:model:`~apps.users.models.user_models.RegisteredCustomerUser`
    is used here rather than the
    :py:model:`~apps.users.models.user_models.BaseUser` model such that
    on saving the form, the
    :py:meth:`~apps.users.models.user_models.RegisteredCustomerUser.save`
    method of the proxy is called.
    """

    class Meta:
        model = RegisteredCustomerUser
        fields = ("email",)


class CustomerProfileCreationForm(ModelForm):
    """Form for creation of a
    :py:model:`~apps.users.models.user_profile_models.CustomerProfile`.
    """

    class Meta:
        model = CustomerProfile
        fields = (
            "first_name",
            "last_name",
        )

    def __init__(self, *arg, **kwarg):
        super(CustomerProfileCreationForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


# Formset for simultaneous creation of RegisteredCustomerUser and
# CustomerProfile
CustomerProfileCreationInlineFormset = inlineformset_factory(
    RegisteredCustomerUser,
    CustomerProfile,
    form=CustomerProfileCreationForm,
    min_num=1,
    max_num=1,
    can_delete=False,
    can_order=False,
)


class CustomerProfileChangeForm(ModelForm):
    """Form for change of a
    :py:model:`~apps.users.models.user_profile_models.CustomerProfile`.
    """

    class Meta:
        model = CustomerProfile
        fields = (
            "first_name",
            "last_name",
        )

    def __init__(self, *arg, **kwarg):
        """Ensures inline formset created using this form cannot be left
        blank.
        """
        super(CustomerProfileChangeForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


# Formset for simultaneous changing of RegisteredCustomerUser and
# CustomerProfile
CustomerProfileChangeInlineFormset = inlineformset_factory(
    RegisteredCustomerUser,
    CustomerProfile,
    form=CustomerProfileChangeForm,
    min_num=1,
    max_num=1,
    can_delete=False,
    can_order=False,
)


class RegisteredCustomerUserAuthenticationForm(AuthenticationForm):
    """Form for authentication of
    :py:model:`~apps.users.models.user_models.RegisteredCustomerUser`.
    """

    pass


class RegisteredCustomerUserPasswordChangeForm(PasswordChangeForm):
    """Form for password change of
    :py:model:`~apps.users.models.user_models.RegisteredCustomerUser`.
    """

    pass


# ====================
# Guest Customer Forms
# ====================
class GuestCustomerUserCreationForm(ModelForm):
    """Form for creation of
    :py:model:`~apps.users.models.user_models:GuestCustomerUser`
    """

    class Meta:
        model = GuestCustomerUser
        exclude = ("is_customer",)


class GuestCustomerProfileCreationForm(ModelForm):
    """Form for creation of
    :py:model:`~apps.users.models.user_profile_models:GuestCustomerProfile`
    """

    class Meta:
        model = GuestCustomerProfile
        exclude = []

        # Hide fields for first_name and last_name and populate them using
        # data from OrderCreationForm in OrderCreateView as it is unnecessary
        # for user to add their name twice.
        # Temporary initial values to get past form validation blank=False.
        widgets = {
            "first_name": HiddenInput(attrs={"value": "temp_first_name"}),
            "last_name": HiddenInput(attrs={"value": "temp_last_name"}),
        }

    def __init__(self, *arg, **kwarg):
        """Ensures inline formset created using this form cannot be left
        blank.
        """
        super(GuestCustomerProfileCreationForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


GuestCustomerProfileCreationInlineFormset = inlineformset_factory(
    GuestCustomerUser,
    GuestCustomerProfile,
    form=GuestCustomerProfileCreationForm,
    min_num=1,
    max_num=1,
    can_delete=False,
    can_order=False,
)
