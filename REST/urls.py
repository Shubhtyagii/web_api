from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from accounts import views
router = DefaultRouter()

router.register('signup', UserViewSet, basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('details/', views.Employee_api, name='Employee_api'),
    path('login/', views.login_view, name='login_view'),
] + router.urls
