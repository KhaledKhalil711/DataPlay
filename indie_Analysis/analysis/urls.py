from django.urls import path
from . import views
urlpatterns = [path('', views.home, name = "home"),
               path("contact/", views.contact, name = "contact"),
               path("login-required/",views.login_required_page, name = "login_required"),
               path("login/",views.login, name = "connecter"),
               path("register/", views.register, name="register"),
               path("q1/",views.q1,name="q1"),
               path("q2/", views.q2, name = "q2"),
               path("q3/", views.q3, name = "q3"),
               ]