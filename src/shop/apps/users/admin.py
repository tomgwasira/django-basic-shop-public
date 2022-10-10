#!/usr/bin/env python
"""Admin classes and routines for **Users* app."""

# Django library imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local application imports
from .forms import *
from .models.user_models import *
from .models.user_profile_models import *


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class CustomerProfileInline(admin.TabularInline):
    """"""

    model = CustomerProfile
    # form = CustomerProfileCreationForm

    def has_delete_permission(self, request, obj=None):
        """"""
        return False


class RegisteredCustomerUserAdmin(UserAdmin):
    """"""

    # add_form = BaseUserCreationForm
    # form = BaseUserChangeForm
    model = RegisteredCustomerUser
    ordering = ("email",)

    # Override default options
    list_display = (
        "email",
        "is_active",
    )
    list_filter = ("is_active",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active",)}),
    )

    # Fields for user creation only
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    inlines = (CustomerProfileInline,)

    def get_queryset(self, *args, **kwargs):
        """Makes admin display subset of
        :py:model:`~apps.users.models.BaseUser` having
        :py:attr:`~apps.users.models.BaseUser.is_superuser` flag set.
        """
        # print(BaseUser.objects.filter(is_customer=True))
        return BaseUser.objects.filter(is_customer=True)


# ================
# Staff Admin Page
# ================
class StaffProfileInline(admin.TabularInline):
    """"""

    model = StaffProfile

    def has_delete_permission(self, request, obj=None):
        """"""
        return False


class StaffUserAdmin(UserAdmin):
    """"""

    # add_form = BaseUserCreationForm
    # form = BaseUserChangeForm
    model = StaffUser
    ordering = ("email",)

    # Override default options
    list_display = (
        "email",
        "is_active",
    )
    list_filter = ("is_active",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active",)}),
    )

    # Fields for user creation only
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    inlines = (StaffProfileInline,)

    def get_queryset(self, *args, **kwargs):
        """Makes admin display subset of
        :py:model:`~apps.users.models.BaseUser` having
        :py:attr:`~apps.users.models.BaseUser.is_superuser` flag set.
        """
        return BaseUser.objects.filter(is_staff=True)


# =========================
# Administrators Admin Page
# =========================
class AdministratorBaseUserAdmin(UserAdmin):
    """"""

    # add_form = BaseUserCreationForm
    # form = BaseUserChangeForm
    model = AdministratorUser
    ordering = ("email",)

    # Override default options
    list_display = (
        "email",
        "is_active",
    )
    list_filter = ("is_active",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active",)}),
    )

    # Fields for user creation only
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    inlines = (StaffProfileInline,)

    def get_queryset(self, *args, **kwargs):
        """Makes admin display subset of
        :py:model:`~apps.users.models.BaseUser` having
        :py:attr:`~apps.users.models.BaseUser.is_superuser` flag set.
        """
        return BaseUser.objects.filter(is_administrator=True)


# =====================
# Superusers Admin Page
# =====================


class SuperuserBaseUserAdmin(UserAdmin):
    """"""

    # add_form = BaseUserCreationForm
    # form = BaseUserChangeForm
    model = SuperuserUser
    ordering = ("email",)

    # Override default options
    list_display = (
        "email",
        "is_active",
    )
    list_filter = ("is_active",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active",)}),
    )

    # Fields for user creation only
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    inlines = (StaffProfileInline,)

    def get_queryset(self, *args, **kwargs):
        """Makes admin display subset of
        :py:model:`~apps.users.models.BaseUser` having
        :py:attr:`~apps.users.models.BaseUser.is_superuser` flag set.
        """
        return BaseUser.objects.filter(is_superuser=True)


# Register UserAdmins
admin.site.register(RegisteredCustomerUser, RegisteredCustomerUserAdmin)
admin.site.register(StaffUser, StaffUserAdmin)
admin.site.register(AdministratorUser, AdministratorBaseUserAdmin)
admin.site.register(SuperuserUser, SuperuserBaseUserAdmin)
