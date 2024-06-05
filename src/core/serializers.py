from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, ProductImage, ProductPrice, Attribute, ProductAttribute


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Category
        fields = ['name', 'description', 'user', 'parent']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class CategoryParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    parent = CategoryParentSerializer()
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'user', 'parent']


class AttributeCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Attribute
        fields = ['name', 'description', 'user']


class AttributeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Attribute
        fields = ['id', 'name', 'description', 'user']



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'description']


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['id', 'coin_amount']


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()
    class Meta:
        model = ProductAttribute
        fields = ['id', "attribute", 'value']


class ProductSerializer(serializers.ModelSerializer):
    price = ProductPriceSerializer()
    attributes = ProductAttributeSerializer(many=True, source='productattribute_set')
    categories = CategorySerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'main_image', 'categories', 'price', 'attributes', 'user']


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    main_image = serializers.ImageField()
    additional_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        required=False
    )
    price = serializers.IntegerField(required=False)
    attributes = serializers.JSONField(required=False)
    categories = serializers.ListField(child=serializers.IntegerField(), required=False)
    