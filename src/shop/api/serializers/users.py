"""Serializers for models defined in :py:mod:`~apps.users.models.user_models`.
"""


from django.core import checks, exceptions, validators

# Django REST Framework Library
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

# Local Application Library
from apps.users.models.user_models import BaseUser, RegisteredCustomerUser
from apps.users.mixins.validation_mixins import (
    CustomerSignUpMixin,
    UserCreationMixin,
)
from apps.users.models.user_profile_models import CustomerProfile, StaffProfile


__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class AuthUserCustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer for basic (non-sensitive) information about authenticated
    user's customer profile.
    """

    class Meta:
        model = CustomerProfile
        fields = ("first_name", "last_name")


class AuthUserStaffProfileSerializer(serializers.ModelSerializer):
    """Serializer for basic (non-sensitive) information about authenticated
    user's staff profile.
    """

    class Meta:
        model = StaffProfile
        fields = ("first_name", "last_name")


class AuthUserSerializer(serializers.ModelSerializer):
    """Serializer for basic (non-sensitive) information about authenticated
    user.
    """

    customer_profile = AuthUserCustomerProfileSerializer()
    staff_profile = AuthUserStaffProfileSerializer()

    class Meta:
        model = BaseUser
        fields = ("customer_profile", "staff_profile")


class SignupCustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ("first_name", "last_name")


class CustomerAccountSerializer(
    UserCreationMixin,
    CustomerSignUpMixin,
    WritableNestedModelSerializer,
):
    """Serializer for customer sign up. While this creates
    :py:model:`~apps.users.models.user_models.RegisteredCustomerUser` objects,
    it also updates any other user account (by creating a
    :py:model:`~apps.users.models.user_profile_models.CustomerProfile`) and
    linking it to the user account.
    """

    password_confirmation = serializers.CharField(write_only=True)
    customer_profile = SignupCustomerProfileSerializer()

    class Meta:
        model = RegisteredCustomerUser  # staff are not actually created but just updated by this serializer
        fields = [
            "email",
            "password",
            "password_confirmation",
            "customer_profile",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "validators": []
            },  # turn off validation of uniqueness of email
        }

    def validate_email(self, value):
        # Check if email exists and if so, if user is staff.
        # If user is staff, only the customer profile will be
        # created and linked to the already existing user.
        # If not, raise validation error for email already existing.
        (
            email_unique_or_is_staff_without_customer_profile,
            error_messages,
        ) = self.check_email_unique_or_is_staff_without_customer_profile(value)
        if not email_unique_or_is_staff_without_customer_profile:
            raise serializers.ValidationError(error_messages)
        return value

    def validate_password(self, value):
        # Check that password is valid
        password_valid, error_messages = self.check_password_valid(value)
        if not password_valid:
            raise serializers.ValidationError(error_messages)
        return value

    def validate(self, data):
        # If staff user exists, check that password entered matches password
        # used for staff account
        if self.staff_user:
            (
                staff_user_password_match,
                error_messages,
            ) = self.check_staff_user_password_match(data["password"])
            if not staff_user_password_match:
                raise serializers.ValidationError({"password": error_messages})

            # No password confirmation necessary. password_confirmation will
            # be popped in create method.

        else:
            # Check that password and password_confirmation match
            password_match, error_messages = self.check_password_match(
                data["password"], data["password_confirmation"]
            )
            if not password_match:
                raise serializers.ValidationError(
                    {"password_confirmation": error_messages}
                )

        return data

    def create(self, validated_data):
        # Extract data for creating nested models
        customer_profile_data = validated_data.pop("customer_profile")

        # Drop fields not to be used in creating object
        validated_data.pop("password_confirmation", None)

        # Drop password so that it can be set using encryption algorithm
        password = validated_data.pop("password", None)

        # Create and link CustomerProfile to BaseUser account. If
        # email does not belong to a BaseUser with is_staff=True, create a
        # RegisteredCustomerUser BaseUser.
        if self.staff_user:
            base_user = self.staff_user

            # Update staff user is_customer to true
            base_user.is_customer = True
            base_user.save()

        else:
            base_user = self.Meta.model(**validated_data)

            if password is not None:
                base_user.set_password(password)
            base_user.save()

        CustomerProfile.objects.create(
            base_user=base_user,
            **customer_profile_data,
        )

        return base_user
