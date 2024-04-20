from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.views import authView, home, custom_password_change, custom_password_change_done
from django.urls import reverse_lazy
from .views import view_profile, edit_profile, create_coin

app_name = 'apps'

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("password_change/", custom_password_change, name="password_change"),
    path("password_change/done/", custom_password_change_done, name="password_change_done"),
    path("profile/", view_profile, name="view_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("create-coin/", create_coin, name="create_coin"),
]
