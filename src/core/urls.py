from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SignUpView
from .views import CategoryViewSet


router = DefaultRouter()

router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('', include(router.urls))
]
