# Generated by Django 3.2.5 on 2022-09-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20220921_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.IntegerField(choices=[(1, 'active'), (2, 'archived'), (3, 'deleted')], default=1),
        ),
    ]
