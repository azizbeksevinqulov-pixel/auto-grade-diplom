from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path("", login_view),  # 👈 ENG MUHIM (root qo‘shildi)

    path("admin/", admin.site.urls),

    path("login/", login_view),
    path("logout/", logout_view),
    path("dashboard/", dashboard),

    path("create/", create_test),
    path("test/", take_test),

    path("users/", users_list),
    path("results/", results_list),
    path("stats/", stats_view),
]
