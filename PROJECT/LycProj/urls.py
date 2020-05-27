from django.contrib import admin
from django.urls import path
from Diary import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('register', views.RegisterFormView.as_view()),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path('', views.MainPage),
]
