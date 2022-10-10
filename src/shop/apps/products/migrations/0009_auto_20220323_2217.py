# Generated by Django 3.2.5 on 2022-03-23 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_headline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='supplier',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='suppliers',
            field=models.ManyToManyField(blank=True, related_name='product_variants', to='products.Supplier'),
        ),
    ]
