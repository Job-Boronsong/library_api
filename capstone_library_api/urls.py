from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library import views as library_views

# Create DRF router and register viewsets
router = DefaultRouter()
router.register(r'books', library_views.BookViewSet, basename='book')
router.register(r'users', library_views.UserViewSet, basename='user')
router.register(r'loans', library_views.LoanViewSet, basename='loan')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # All API endpoints
    path('api-auth/', include('rest_framework.urls')),  # DRF browsable API login/logout
]

# Optional: Add a simple root page
from django.http import JsonResponse
def home(request):
    return JsonResponse({"message": "Welcome to the Capstone Library API"})

urlpatterns.insert(0, path('', home))  # Root URL shows a welcome JSON
