# Generated by Django 5.0.6 on 2024-06-04 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Attribute Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Attribute Description')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Product Name')),
                ('description', models.TextField(verbose_name='Product Description')),
                ('main_image', models.ImageField(upload_to='products/main_images/', verbose_name='Main Image')),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Attribute Value')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.attribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'unique_together': {('product', 'attribute')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(related_name='products', through='core.ProductAttribute', to='core.attribute'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/additional_images/')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_amount', models.IntegerField(verbose_name='Product Price Coin Amount')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='core.product')),
            ],
        ),
    ]
