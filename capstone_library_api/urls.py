from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'borrow-records', views.BorrowRecordViewSet, basename='borrowrecord')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),  # Token authentication
]
