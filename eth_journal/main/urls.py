from django.urls import path,include
from .views import index,login,StudentsAPIView,TestAuthAPIView

app_name = 'main'
urlpatterns = [
    path('index/',index),
    path('login/',login),
    path('api/students/',StudentsAPIView.as_view()),
    path('api/testauth/',TestAuthAPIView.as_view())
]