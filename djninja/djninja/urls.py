from django.contrib import admin
from django.urls import path
from nums.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls)
]
