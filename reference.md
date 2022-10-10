# Reference

- If you use a reference to a model, follow it with object. Just to make it less ambiguous.

./dev_tools/scripts/dumpdata.sh

## Timing

```
import time
start = time.time()
end = time.time()
print(end - start)
```

Password: django-basic-shop123

# Imports

**author** = "Thomas Gwasira"
**date** = "July 2021"
**version** = "0.1.0"
**maintainer** = "Thomas Gwasira"
**email** = "tomgwasira@gmail.com"
**status** = "Development"

from shop.routines import _
from apps.products.models.product_models import _
p = ProductVariant.objects.all().first()
to_json(p)

from shop.routines import \*

> > > from apps.users.models.user_profile_models import \*
> > > rc = CustomerProfile.objects.all().first()
> > > to_dict(rc)

# Pytest

pytest tests/unit/apps/products/models/test_product_models.py -s

# Paths for linking docstrings

:py:class:`~apps.products.admin.CategoryAdmin`
:py:model:`~apps.products.models.product_models.Category`
:py:attr:`~apps.products.models.product_models.Category.name`
:py:meth:`~tests.unit.apps.products.models.test_product_models.TestCategory.test_get_absolute_url

# 79 characters (PEP code length)

...............................................................................

# 72 characters (PEP docstrings and comment length)

........................................................................

# Exporting database tables into fixtures

django-admin dumpdata --indent 2 --output fixtures/

django-admin dumpdata products --indent 2 --output apps/products/fixtures/products.json
django-admin dumpdata products --indent 2 --output apps/products/fixtures/products.json
django-admin dumpdata products.product --indent 2 --output apps/products/fixtures/product.json

django-admin dumpdata auth.user --indent 2 --output apps/users/fixtures/db_admin_fixture.json
django-admin dumpdata products.category --indent 2 --output apps/products/fixtures/products_category_fixture.json
django-admin dumpdata products.productvariant --indent 2 --output apps/products/fixtures/products_productvariant_fixture.json
django-admin dumpdata products.supplier --indent 2 --output apps/products/fixtures/products_supplier_fixture.json
django-admin dumpdata products.categoryheroimage --indent 2 --output apps/products/fixtures/products_categoryheroimage_fixture.json
django-admin dumpdata products.category --indent 2 --output apps/products/fixtures/products\_\_fixture.json
django-admin dumpdata products.optiontype --indent 2 --output apps/products/fixtures/products_optiontype_fixture.json
django-admin dumpdata products.optionvalue --indent 2 --output apps/products/fixtures/products_optionvalue_fixture.json
django-admin dumpdata products.supplier --indent 2 --output apps/products/fixtures/products_supplier_fixture.json
django-admin dumpdata products.brand --indent 2 --output apps/products/fixtures/products_brand_fixture.json

# Loading database tables from fixtures

django-admin loaddata auth_user.json
django-admin loaddata products_category_fixture.json
django-admin loaddata products_optiontype_fixture.json
django-admin loaddata products_optionvalue_fixture.json
django-admin loaddata products_supplier_fixture.json
django-admin loaddata products_product_fixture.json
django-admin loaddata products_brand_fixture.json
