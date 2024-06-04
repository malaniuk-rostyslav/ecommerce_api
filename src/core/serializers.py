from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, ProductImage, ProductPrice, Attribute, ProductAttribute


class UserSerializer(serializers.ModelSerializer):
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