#!/usr/bin/env python
"""Models for system warnings."""

# Django library imports
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields import BooleanField, DateTimeField, TextField


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class SystemWarning(models.Model):
    """System warning."""

    title = models.CharField(max_length=1000, unique=True)
    message = TextField(blank=True, max_length=1000)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_deleted = BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ("updated_at",)
        verbose_name = "Warning"
        verbose_name_plural = "Warnings"

    def __str__(self):
        """Returns title of the
        :py:model:`~apps.system.warnings.models.Warning` object as its
        string representation.
        """
        return f"{self.title}"
