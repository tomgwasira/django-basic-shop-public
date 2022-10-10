#!/usr/bin/env python
"""Signal handlers for various signals in **Products** app."""

# Django library imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local application imports
from .models.product_models import OptionValue, ProductVariant


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


# @receiver(post_save, sender=ProductVariant)
# def create_sku_object(sender, instance, created, **kwargs):
#     # Check if ProductVariant has been created
#     if created:
#         # Only create Sku if adding new ProductVariant
#         if instance._state.adding:
#             new_sku = Sku(
#                 sku_no=instance.sku_no,
#                 product_variant_summary=instance.product_variant_summary,
#             )

#             new_sku.save()

#         # # If not adding new ProductVariant, check if sku_no changed
#         # else:
#         #     if not (Sku.objects.filter(instance.sku_no)).exists():


# # TODO: m2m_changed to see if sku_no changed or consider above comment or consider a flag which checks if sku_no has changed and then is reset when the new Sku has been created
