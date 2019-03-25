from django.contrib import admin
from django.urls import path

from core.views import auth


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', auth.register),
]
