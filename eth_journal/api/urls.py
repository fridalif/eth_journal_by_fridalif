from django.urls import path, include
from .views import RegisterRequestsAPIView

app_name = 'api'
urlpatterns = [
    path('register_requests/',RegisterRequestsAPIView.as_view(),name='register_requests')
]
