#!/usr/bin/env python
"""Miscellaneous routines for use in project."""

# Standard library imports
from itertools import chain
import collections
from json import dumps
from locale import currency
from time import time

# Django library imports
from django.db.models.fields import DateTimeField, DecimalField
from django.db.models.fields.related import ForeignKey, OneToOneField

# Third-party library imports
from djmoney.models.fields import MoneyField


__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


def autoslug_slugify(content):
    """Replace all non-alphanumeric characters with a hyphen '-' and
    turn all letters into lowercase.

    This function is used by ``AutoSlugField`` to generate slugs for
    models.

    Args:
        content (str): The content to be slugified.

    Returns:
        str: Original content but lowercase and with all
        non-alphanumeric characters converted into a hyphen.
    """

    for c in content:
        if not c.isalnum():
            content = content.replace(c, "-")

    return content.lower()


def to_json(instance):
    """Return JSON representation of model instance.

    In the case of related object fields, this function makes a
    recursive call to the :py:func:`~shop.routines.to_json` function to
    generate a JSON object for the related instance such that a nested
    JSON structure is obtained.

    This function is mainly used to create JSON data for records of
    history of objects.

    The following serializations are performed in order for the
    intermediary dictionary representation of the model instance to be
    convertible into a JSON object:
        * ``DateTimeField`` attributes are serialized into their string
            representations.
        * ``MoneyField`` attributes are serialized into two independent
            values ``<fieldname>`` and ``<fieldname>_currency``.
            Furthermore, ``<fieldname>`` holds the float value of
            the ``Decimal`` amount and ``<fieldname>_currency`` holds
            the string representation of the ``Currency`` object
            attached to the ``Money`` object. This is consistent with
            the result that would be obtained if the command
            ``django-admin dumpdata`` was run.
        * Values of type ``Decimal`` are typecasted into ``float``.

    Args:
        instance (Model): Model instance whose dictionary representation
            is to be obtained.

    Returns:
        Json: JSON representation of model instance.
    """
    opts = instance._meta
    data = {}

    # Non-m2m fields
    for f in chain(opts.concrete_fields, opts.private_fields):
        if isinstance(f, ForeignKey) or isinstance(f, OneToOneField):
            data[f.name] = to_json(getattr(instance, f.name))

        # Serialize certain data types which are not, by default, JSON
        # serializable.
        # Before data can be typecasted, a check must first be done to
        # see that it is not None.
        else:
            if isinstance(f, DateTimeField):
                date = getattr(instance, f.name, None)
                data[f.name] = str(date) if date else None

            elif isinstance(f, MoneyField):
                money = getattr(instance, f.name)
                amount = getattr(money, "amount", None)
                currency = getattr(money, "currency", None)

                data[f.name] = float(amount) if amount else None
                data[f"{f.name}_currency"] = (
                    str(currency) if currency else None
                )

            elif isinstance(f, DecimalField):
                value = getattr(instance, f.name, None)
                data[f.name] = float(value) if value else None

            else:
                data[f.name] = getattr(instance, f.name)

    # M2m fields
    for f in opts.many_to_many:
        data[f.name] = [to_json(i) for i in f.value_from_object(instance)]
    return dumps(data)
