    def test_is_active_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("is_active").default

    def test_slug_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("slug")._populate_from == "name"
        assert option_value._meta.get_field("slug").overwrite
        assert option_value._meta.get_field("slug").unique

    def test_created_at_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("created_at").auto_now_add

    def test_updated_at_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert option_value._meta.get_field("updated_at").auto_now

    def test_uuid_field_attributes(self):
        option_value = OptionValue.objects.get(id=1)

        assert not option_value._meta.get_field("uuid").editable
