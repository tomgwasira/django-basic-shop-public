#!/usr/bin/env python
"""URLconf for Users app."""

from django.urls import path

from . import views

__author__ = "Thomas Gwasira"
__date__ = "December 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


app_name = "users"
urlpatterns = [
    path("login/", views.CustomerLoginView.as_view(), name="customer_login"),
    path(
        "logout/",
        views.CustomerLogoutView.as_view(),
        name="customer_logout",
    ),
    path(
        "signup/",
        views.CustomerSignupView.as_view(),
        name="customer_signup",
    ),
    path(
        "update/",
        views.CustomerUpdateView.as_view(),
        name="customer_update",
    ),
    path(
        "password_change/",
        views.CustomerPasswordChangeView.as_view(),
        name="customer_password_change",
    ),
    path(
        "password_change/done/",
        views.CustomerPasswordChangeDoneView.as_view(),
        name="customer_password_change_done",
    ),
    path(
        "deactivate/",
        views.CustomerDeactivateView.as_view(),
        name="customer_deactivate",
    ),
    path(
        "deactivate/done/",
        views.CustomerDeactivateDoneView.as_view(),
        name="customer_deactivate_done",
    ),
    path(
        "deactivate/not_allowed/",
        views.CustomerDeactivateNotAllowedView.as_view(),
        name="customer_deactivate_not_allowed",
    ),
]
