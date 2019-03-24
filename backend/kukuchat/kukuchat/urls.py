from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views

from core.views import auth, provider


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.obtain_auth_token),
    path('api/register/', auth.register),
    path('api/provider/get_avaliable_providers/', provider.get_avaliable_providers),
    path('api/provider/<provider_name>/<provider_func_name>/', provider.provider_interact),
]
