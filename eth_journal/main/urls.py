from django.urls import path,include
from .views import index

app_name = 'main'
urlpatterns = [
    path('index/',index)
]