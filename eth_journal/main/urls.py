from django.urls import path,include
from .views import index,StudentsAPIView

app_name = 'main'
urlpatterns = [
    path('index/',index),
    path('api/students/',StudentsAPIView.as_view())
]