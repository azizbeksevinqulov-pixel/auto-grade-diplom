from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [

    # ===== ROOT =====
    path("", login_view),

    # ===== AUTH =====
    path("login/", login_view),
    path("register/", register_view),
    path("logout/", logout_view),

    # ===== ADMIN =====
    path("admin/", admin.site.urls),
    path("admin-panel/", admin_panel),
    path("create-admin/", create_admin),

    # ===== TEST SYSTEM =====
    path("create/", create_test),
    path("test/", take_test),

    # ===== DATA =====
    path("users/", users_list),
    path("results/", results_list),
    path("stats/", stats_view),

]
