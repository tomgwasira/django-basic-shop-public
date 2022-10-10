#!/usr/bin/env python
"""Views for search engine."""

from typing import List
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView


from apps.products.models.product_models import Category, Product


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class ProductSearchView(ListView):

    template_name = "products/search_result.html"
    context_object_name = "products"

    def get_queryset(self):
        self.query = self.request.GET.get("q")

        if self.query:
            category_matches = Category.objects.filter(
                Q(name__contains=self.query)
            )
            category_matches_and_descendants = []

            for category in category_matches:
                category_matches_and_descendants.append(category)
                for descendant in category.get_descendants():
                    category_matches_and_descendants.append(descendant)

            products = Product.objects.filter(
                Q(name__contains=self.query)
                | Q(category__in=category_matches_and_descendants)
                | Q(description__contains=self.query)
                | Q(tag__name__contains=self.query)
            ).distinct()

        else:
            products = Product.objects.none()

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["query"] = self.query

        return context
