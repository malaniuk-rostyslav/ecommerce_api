from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Category Name')
    description = models.TextField(verbose_name='Category Description')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Attribute Name')
    description = models.TextField(blank=True, null=True, verbose_name='Attribute Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Product Name')
    description = models.TextField(verbose_name='Product Description')
    main_image = models.ImageField(upload_to='products/main_images/', verbose_name='Main Image')
    categories = models.ManyToManyField(Category, blank=True, related_name='products')
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute', related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductPrice(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='price')
    coin_amount = models.IntegerField(verbose_name='Product Price Coin Amount')

    def __str__(self):
        return f"{self.product.name}: {self.coin_amount} units"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/additional_images/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image {self.id} for {self.product.name}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Attribute Value')

    class Meta:
        unique_together = ('product', 'attribute')

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
