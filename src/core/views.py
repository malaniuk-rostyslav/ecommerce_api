from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Attribute
from .serializers import UserSerializer, CategoryCreateSerializer, CategorySerializer, AttributeCreateSerializer, AttributeSerializer

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
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
        if self.action == 'create' or self.action == 'update':
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
