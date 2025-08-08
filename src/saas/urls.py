from django.contrib import admin
from django.urls import path

from auth import views as auth_view
from .views import home_page_view, x_page_view

urlpatterns = [
    path("", home_page_view),
    path("login/", auth_view.login_view),
    path("register/", auth_view.register_view),
    path("x/", x_page_view),
    path('admin/', admin.site.urls),
]
