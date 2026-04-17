from django.urls import path
from core.views import test_page

urlpatterns = [
    path("", test_page),
]
