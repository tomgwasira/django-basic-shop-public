# Generated by Django 3.2.5 on 2022-03-13 17:03

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20220312_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='position',
            field=models.DecimalField(decimal_places=30, default=Decimal('1000000'), max_digits=40),
        ),
        migrations.AlterField(
            model_name='categoryheroimage',
            name='position',
            field=models.DecimalField(decimal_places=30, default=Decimal('1000000'), max_digits=40),
        ),
        migrations.AlterField(
            model_name='optiontype',
            name='position',
            field=models.DecimalField(decimal_places=30, default=Decimal('1000000'), max_digits=40),
        ),
        migrations.AlterField(
            model_name='optionvalue',
            name='option_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_values', to='products.optiontype'),
        ),
        migrations.AlterField(
            model_name='product',
            name='option_types',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.OptionType'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='position',
            field=models.DecimalField(decimal_places=30, default=Decimal('1000000'), max_digits=40),
        ),
    ]