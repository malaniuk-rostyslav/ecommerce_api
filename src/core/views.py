from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Attribute, Product, ProductPrice, ProductAttribute, ProductImage
from .serializers import UserCreateSerializer, CategoryCreateSerializer, CategorySerializer, AttributeCreateSerializer, AttributeSerializer, ProductCreateSerializer, ProductSerializer
from django.db import IntegrityError


class SignUpView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CategoryCreateSerializer
        elif self.action == 'destroy':
            return Response(status=status.HTTP_204_NO_CONTENT)
        return CategorySerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        response_serializer = CategorySerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        response_serializer = CategorySerializer(instance)
        return Response(response_serializer.data)


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return AttributeCreateSerializer
        elif self.action == 'destroy':
            return Response(status=status.HTTP_204_NO_CONTENT)
        return AttributeSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        response_serializer = AttributeSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        response_serializer = AttributeSerializer(instance)
        return Response(response_serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProductCreateSerializer
        elif self.action == 'destroy':
            return Response(status=status.HTTP_204_NO_CONTENT)
        return ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        additional_images = validated_data.get('additional_images')
        price = validated_data.get('price', None)
        attributes = validated_data.get('attributes', {})
        categories = validated_data.get('categories', [])

        # Check if categories exist in DB
        if categories and not Category.objects.filter(pk__in=categories).count() == len(categories):
            return Response({"error": "Invalid categories"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if attributes exist in DB
        if attributes:
            invalid_attributes = [name for name in attributes.keys() if not Attribute.objects.filter(name=name).exists()]
            if invalid_attributes:
                return Response({"error": "Wrong attributes"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Product
        product = Product.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            main_image=validated_data['main_image'],
            user=request.user
        )

        # Add categories to Product
        if categories:
            product.categories.set(categories)
        
        # Add additional images
        for image in additional_images:
            ProductImage.objects.create(product=product, image=image)

        # Add Price
        ProductPrice.objects.create(product=product, coin_amount=price)

        # Add attributes
        for attribute_name, value in attributes.items():
            attribute_instance, _ = Attribute.objects.get_or_create(name=attribute_name, user=request.user)
            ProductAttribute.objects.create(product=product, attribute=attribute_instance, value=value)

        response_serializer = ProductSerializer(product)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        additional_images = validated_data.get('additional_images')
        price = validated_data.get('price', None)
        attributes = validated_data.get('attributes', {})
        categories = validated_data.get('categories', [])

        # Update Product fields if they are in FORM data
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.main_image = validated_data.get('main_image', instance.main_image)
        instance.save()

        # Update categories if they are in FORM data
        if categories:
            instance.categories.set(categories)

        # Update additional_images if they are in FORM data
        if additional_images:
            instance.additional_images.all().delete()
            for image in additional_images:
                ProductImage.objects.create(product=instance, image=image)

        # Update Price if it is in FORM data
        if price :
            if hasattr(instance, 'price'):
                instance.price.coin_amount = price
                instance.price.save()
            else:
                ProductPrice.objects.create(product=instance, coin_amount=price)

        # Update attributes if they are in FORM data
        if attributes:
            instance.productattribute_set.all().delete()
            for attribute_name, value in attributes.items():
                attribute_instance, _ = Attribute.objects.get_or_create(name=attribute_name)
                ProductAttribute.objects.create(product=instance, attribute=attribute_instance, value=value)

        response_serializer = ProductSerializer(instance)
        return Response(response_serializer.data)
