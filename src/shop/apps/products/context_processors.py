#!/usr/bin/env python
"""Context processors for products app."""


from .models.product_models import Category


__author__ = "Thomas Gwasira"
__date__ = "July 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"



def get_main_categories(request):
    """Returns a dictionary of all main categories (i.e. depth = 1) which places them in the context.
    
    These are to be used to create a navbar where the list of main categories is iterated over and it's descendants are obtained to create styled dropdowns.
    """

    main_categories = Category.objects.filter(depth=1)

    # Print objects for use in fixtures
    # all_categories = Category.objects.all()
    # print('[')
    # for category in all_categories:
    #     print('  {')
    #     print('    "model": "products.category",')
    #     print('    "pk": {0},'.format(category.id)) # consider making this 1 or something
    #     print('    "fields": {')
    #     print('        "lft": {0},'.format(category.lft))
    #     print('        "rgt": {0},'.format(category.rgt))
    #     print('        "tree_id": {0},'.format(category.tree_id))
    #     print('        "depth": {0},'.format(category.depth))

    #     print('        "name": "{0}",'.format(category.name))
    #     print('        "slug": "{0}",'.format(category.slug))
    #     print('        "description": "{0}",'.format(category.description))
    #     print('        "created": "{0}",'.format(category.created))
    #     print('        "updated": "{0}"'.format(category.updated))
    #     print('    }')
    #     print('  },')
    
    # print(']')

    return dict(main_categories = main_categories)