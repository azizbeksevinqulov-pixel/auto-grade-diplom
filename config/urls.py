from django.contrib import admin
from django.urls import path
from core.views import test_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", test_page),
]
