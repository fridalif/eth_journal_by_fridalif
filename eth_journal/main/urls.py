from django.urls import path, include
from .views import index, register, lessons_plan, profile, settings, admin_requests_view, hours_plan_view, raiting, \
    password_recovery, add_lessons_teacher_view
from django.contrib.auth import views

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='main:index'), name='logout'),
    path('register/', register, name='register'),
    path('lessons_plan/', lessons_plan, name='lessons_plan'),
    path('profile/<slug:profile_slug>/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('admin_requests/', admin_requests_view, name='admin_requests'),
    path('hours_plan/', hours_plan_view, name='hours_plan'),
    path('raiting/', raiting, name='raiting'),
    path('password_recovery/', password_recovery, name='password_recovery'),
    path('add_lessons/', add_lessons_teacher_view, name="add_lessons")
]
