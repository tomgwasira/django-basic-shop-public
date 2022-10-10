#!/usr/bin/env python
"""Views for Users app."""

# Django library imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import UpdateView

# Local application imports
from .forms import *
from .models.user_models import *


class CustomerLoginView(LoginView):
    """LoginView overriden for better scalability. Could have gone route of calling the LoginView in the urls directly with some arguments
    e.g. custom template."""

    template_name = "users/login.html"
    form_class = RegisteredCustomerUserAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """Overriden. Redirects to homepage.
        Used just for safety. They shouldn't even see a button allowing them to login if they're already loggedin"""
        return reverse_lazy("index")

    def post(self, request):
        """Redirects to same page if failed using https://stackoverflow.com/questions/39560175/redirect-to-same-page-after-post-method-using-class-based-views"""
        email = request.POST[
            "username"
        ]  # note, email is actually username in Authentication form given the reset we did
        password = request.POST["password"]
        form = self.get_form()
        # TODO: Why is get_form() working. Is it defined in the function that AuthenticationView is inheriting?
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(
                    self.request.POST.get("next", reverse_lazy("index"))
                )
            else:
                return HttpResponse("Inactive user.")
        else:
            # https://stackoverflow.com/questions/31065796/mutiple-forms-with-class-based-view-how-to-show-errors-at-the-same-page

            # context = {}
            # context["form"] = form
            # return render(request, 'template', context)
            # return self.invalid_login(self, form=form) # This gave csrf error ------link above.
            return render(
                request, self.template_name, {"form": form}
            )  # 293 votes


class CustomerLogoutView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy("users:customer_login")
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        """Does not throw error if user is not logged in.
        Todo: Check if we should also do this in post.
        might want to Redirect user to page they were previously on
        but will need to first check if they have authorisation to view the page otherwise home
        """
        logout(request)
        return redirect(self.request.GET.get("next", reverse_lazy("index")))


class CustomerSignupView(CreateView):
    """Warning:
    Use correct form otherwise save() method will not be called"""

    # TODO: Some type of logout required functionality
    form_class = RegisteredCustomerUserCreationForm
    template_name = "users/signup_form.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerSignupView, self).get_context_data(**kwargs)

        if self.request.POST:
            context[
                "customer_creation_inline_formset"
            ] = CustomerProfileCreationInlineFormset(self.request.POST)
        else:
            context[
                "customer_creation_inline_formset"
            ] = CustomerProfileCreationInlineFormset()
        return context

    def form_invalid(self, request, form):
        """If the form is invalid, render the invalid form."""
        print("Invalidatos")
        # https://stackoverflow.com/questions/31065796/mutiple-forms-with-class-based-view-how-to-show-errors-at-the-same-page
        # TODO: DEPRECATED
        return render(
            self.request, self.template_name, self.get_context_data(form=form)
        )

    def form_valid(self, form):
        # TODO: Use form instead
        context = self.get_context_data()

        customer_creation_inline_formset = context[
            "customer_creation_inline_formset"
        ]

        if form.is_valid() and customer_creation_inline_formset.is_valid():
            print(customer_creation_inline_formset.cleaned_data)
            # Save both parent and inline
            obj = form.save()
            customer_creation_inline_formset.instance = obj
            customer_creation_inline_formset.save()

            # Get user details so that they can be logged in automatically
            # Get from cleaned_data otherwise you will get hashed password
            # if you try to access object attributes
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")

            # Log user in automatically after signup
            # First logs out if a user was logged in
            new_user = authenticate(email=email, password=password)
            login(self.request, new_user)

            return redirect(
                self.request.GET.get("next", reverse_lazy("index"))
            )

        else:
            return self.form_invalid(self, form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """Based on https://stackoverflow.com/questions/32575535/django-updateview-with-inline-formsets-trying-to-save-duplicate-records
    and https://stackoverflow.com/questions/55892832/unique-constraint-failed-auth-user-username-while-updating-user-info
    https://stackoverflow.com/questions/17561736/django-updateview-without-pk-in-url
    No pk becuase of security. want only current user"""

    login_url = reverse_lazy("users:customer_login")
    redirect_field_name = "redirect_to"

    model = RegisteredCustomerUser
    form_class = RegisteredCustomerUserChangeForm  # TODO: Change this!!!!
    template_name = "users/manage_account_form.html"
    success_template = "users/update_done.html"
    update_not_allowed_template = "users/update_not_allowed.html"
    # TODO: Remove all self.object for obj
    def get_object(self, request, *args, **kwargs):
        # TODO: Go back to just request.user
        # TODO: raise 404 if user is None or not authenticated
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_staff or user.is_administrator or user.is_superuser):
            self.object = self.get_object(self)
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            customer_change_inline_formset = (
                CustomerProfileChangeInlineFormset(instance=self.object)
            )

            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    customer_change_inline_formset=customer_change_inline_formset,
                )
            )

        else:
            return render(None, self.update_not_allowed_template, {})

    # def get_success_url(self):
    #     self.success_url = "/"
    #     return self.success_url

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        customer_change_inline_formset = CustomerProfileChangeInlineFormset(
            self.request.POST, instance=self.object
        )

        if form.is_valid() and customer_change_inline_formset.is_valid():
            return self.form_valid(form, customer_change_inline_formset)
        return self.form_invalid(form, customer_change_inline_formset)

    def form_valid(self, form, customer_change_inline_formset):
        obj = form.save()
        customer_change_inline_formset.instance = obj
        customer_change_inline_formset.save()
        return render(None, self.success_template, {})
        # return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, customer_change_inline_formset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                customer_change_inline_formset=customer_change_inline_formset,
            )
        )


class CustomerPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    login_url = reverse_lazy("users:customer_login")
    redirect_field_name = "redirect_to"

    form_class = RegisteredCustomerUserPasswordChangeForm
    success_url = reverse_lazy("users:customer_password_change_done")
    template_name = "users/password_change_form.html"


class CustomerPasswordChangeDoneView(
    LoginRequiredMixin, PasswordChangeDoneView
):
    login_url = reverse_lazy("users:customer_login")
    redirect_field_name = "redirect_to"

    template_name = "users/password_change_done.html"


class CustomerDeactivateView(LoginRequiredMixin, View):
    """Deactivates a customer account until such a time when it can
    be permanently deleted.
    """

    login_url = reverse_lazy("users:customer_login")
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        # TODO: raise 404 if user is None or not authenticated
        # TODO: Should I pass request in render. Check if this works
        # TODO: Double check difference between this and using update() and what signals are called when
        user = self.request.user
        # Do not deactivate staff or administrator or superuser
        if not (user.is_staff or user.is_administrator or user.is_superuser):
            user.is_active = False
            user.save()
            logout(request)

            return JsonResponse(
                {"next_url": reverse_lazy("users:customer_deactivate_done")}
            )

        else:
            return JsonResponse(
                {
                    "next_url": reverse_lazy(
                        "users:customer_deactivate_not_allowed"
                    )
                }
            )


class CustomerDeactivateDoneView(TemplateView):
    """For redirecting to customer done page. Might want another solution like a popup."""

    template_name = "users/deactivate_done.html"


class CustomerDeactivateNotAllowedView(TemplateView):
    """For redirecting to customer not allowed page. Might want another solution like a popup."""

    template_name = "users/deactivate_not_allowed.html"
