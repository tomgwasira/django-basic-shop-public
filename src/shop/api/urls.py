#!/usr/bin/env python
"""URLconf for API app."""

# Django library
# Django library imports
from django.urls import include, path

# Django REST Framework library
# Django REST framework library imports
from rest_framework.routers import DefaultRouter

# Third-party libraries
from api.admin.views.products import (
    BrandAdminViewset,
    CategoryAdminViewSet,
    OptionTypeAdminViewSet,
    ProductAdminViewset,
    SupplierAdminViewset,
)
from api.views.products import CategoriesViewset, ProductsViewSet
from api.views.users import (
    AuthUserView,
    CustomerAccountView,
    CustomerSignupView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"

router = DefaultRouter()
router.register(
    r"categories",
    CategoriesViewset,
)
router.register(
    r"products",
    ProductsViewSet,
)
router.register(
    r"admin/option-types",
    OptionTypeAdminViewSet,
)
router.register(r"admin/categories", CategoryAdminViewSet)
router.register(r"admin/brands", BrandAdminViewset)
router.register(r"admin/suppliers", SupplierAdminViewset)
router.register(r"admin/products", ProductAdminViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
    path("signup/", CustomerSignupView.as_view()),
    path("auth-user/", AuthUserView.as_view()),
    path("account/", CustomerAccountView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
