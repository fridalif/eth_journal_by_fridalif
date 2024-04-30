from django.urls import path, include
from .views import index,register
from django.contrib.auth import views

app_name = 'main'
urlpatterns = [
    path('index/', index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='/index/'), name='logout'),
    path('register/', register, name='register'),
]
