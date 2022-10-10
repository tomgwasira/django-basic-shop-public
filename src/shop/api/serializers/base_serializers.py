"""Base serializers for use in creating other serializers."""

# Django REST Framework Library
# Django REST Framework library
from rest_framework import serializers

__author__ = "Thomas Gwasira"
__date__ = "2022"
__version__ = "0.1.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


class PrimaryKeyRelatedFieldWithDetailedRepresentation(
    serializers.PrimaryKeyRelatedField
):
    def to_representation(self, value):
        # if self.pk_field is not None:
        #     return self.pk_field.to_representation(value.pk)
        return value.get_pk_related_field_data()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
