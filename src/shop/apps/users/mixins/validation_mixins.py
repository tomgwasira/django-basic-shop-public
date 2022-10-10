from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from apps.users.models.user_models import BaseUser


class UserCreationMixin:
    """Mixin for basic user creation routines."""

    def check_password_valid(self, password):
        """Check that given password meets criteria specified.

        Args:
            password (str): Password value.

        Returns:
            (bool, list/None): Tuple where first element is a Boolean
                indicating whether the password is valid or not and the second
                element is either a list of error messages if the password is
                invalid or None.
        """

        if password:
            try:
                password_validation.validate_password(password)
                return (True, None)
            except ValidationError as error:
                return (False, error.messages)

    def check_password_match(self, password1, password2):
        """Check that two passwords match.

        Args:
            password1 (str): First password to be compared.
            password2 (str): Second password to be compared.

        Returns:
            (bool, str/None): Tuple where first element is a Boolean
                indicating whether the passwords match and the second element
                is either an error message if the passwords don't match or
                None.
        """

        if password1 != password2:
            return (False, "Passwords do not match.")
        return (True, None)


class CustomerSignUpMixin:
    """Mixin for basic registered customer sign up routines."""

    def check_email_unique_or_is_staff_without_customer_profile(self, email):
        """Check if an email address provided for sign up of a registered
        customer user is unique or belongs to a staff user without a customer
        profile already.

        Also add variable ```staff_user``` with instance of staff user or
        ```None``` to ```self```. This avoids having to query the database
        again when the user is needed later.

        Args:
            email (str): Email for to be used for signing up registered
                customer user.

        Returns:
            (bool, str/None): Tuple where first element is a Boolean
                indicating whether the email is either unique or belongs to a
                staff user and the second element is either an of error
                messages if the email doesn't meet the stated criterial or
                None.
        """
        self.staff_user = None
        if user := BaseUser.objects.filter(email=email).first():
            # Cannot have more than one user as email is unique
            if user.is_staff and not getattr(user, "customer_profile", None):
                self.staff_user = user
                return (True, None)
            else:
                return (
                    False,
                    "A user with this email address already exists.",
                )
        else:
            return (True, None)

    def check_staff_user_password_match(self, password):
        """Check if password matches that of the staff user assigned to
        ```self.staff_user```.

        Args:
            password (str): Password to be compared with staff user password.

        Returns:
            (bool, str/None): Tuple where first element is a Boolean
                indicating whether the passwords match and the second element
                is either an error message if the passwords don't match or
                None.

        Warning:
            This method assumes that the ```self.staff_user``` exists. If not,
            it will result in an error which implies incorrect usage as the
            check for whether staff user password match should always be
            called after the check for whether the user is staff.
        """

        if self.staff_user.check_password(password):
            return (True, None)
        else:
            return (
                False,
                "Email entered matches a staff user account. Use the same"
                + "password for the staff account.",
            )
