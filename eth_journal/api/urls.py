from django.urls import path, include
from .views import RegisterRequestsAPIView, LessonAPIView

app_name = 'api'
urlpatterns = [
    path('register_requests/', RegisterRequestsAPIView.as_view(), name='register_requests'),
    path('lessons/', LessonAPIView.as_view(), name="lessons"),
    path('lessons/<int:lesson_id>/',LessonAPIView.as_view(),name='lesson')
]
