from django.urls import path, include
from .views import index, register, lessons_plan, profile
from django.contrib.auth import views

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='main:index'), name='logout'),
    path('register/', register, name='register'),
    path('lessons_plan/', lessons_plan, name='lessons_plan'),
    path('profile/<slug:profile_slug>/', profile, name='profile')
]
