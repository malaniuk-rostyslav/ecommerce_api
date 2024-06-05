from django.db import models
from django.contrib.auth.models import User

class TimeStampMixin(models.Model):
    """Default timestamp mixin class could be used only for the inheritance"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True, verbose_name='Category Name')
    description = models.TextField(verbose_name='Category Description')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attribute(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True, verbose_name='Attribute Name')
    description = models.TextField(blank=True, null=True, verbose_name='Attribute Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(TimeStampMixin):
    name = models.CharField(max_length=255, verbose_name='Product Name')
    description = models.TextField(verbose_name='Product Description')
    main_image = models.ImageField(upload_to='products/main_images/', verbose_name='Main Image')
    categories = models.ManyToManyField(Category, blank=True, related_name='products')
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute', related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductPrice(TimeStampMixin):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='price')
    coin_amount = models.IntegerField(verbose_name='Product Price Coin Amount')

    def __str__(self):
        return f"{self.product.name}: {self.coin_amount} units"


class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/additional_images/')

    def __str__(self):
        return f"Image {self.id} for {self.product.name}"


class ProductAttribute(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Attribute Value')

    class Meta:
        unique_together = ('product', 'attribute')

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
