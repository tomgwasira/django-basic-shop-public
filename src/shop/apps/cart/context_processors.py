#!/usr/bin/env python
"""Context processors for cart app."""


from .cart import Cart


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


def get_cart(request):
    """Returns a dictionary containing a cart object containing information of the current session.

    :return: Dictionary containing a cart object containing information of the current session
    :rtype: dict
    """
    return {"cart": Cart(request)}
