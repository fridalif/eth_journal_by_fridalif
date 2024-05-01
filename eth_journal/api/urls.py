from django.urls import path, include
from .views import RegisterRequestsAPIView, LessonAPIView, LessonStudentInfoAPIView,SubjectAPIView,GroupAPIView

app_name = 'api'
urlpatterns = [
    path('register_requests/', RegisterRequestsAPIView.as_view(), name='register_requests'),
    path('lessons/', LessonAPIView.as_view(), name="lessons"),
    path('lessons/<int:lesson_id>/', LessonAPIView.as_view(), name='lesson'),
    path('lesson_student_info/', LessonStudentInfoAPIView.as_view(), name='lesson_student_info'),
    path('lesson_student_info/<int:lesson_id>/', LessonStudentInfoAPIView.as_view(),
         name='lesson_student_info_per_lesson'),
    path('lesson_student_info/<int:lesson_id>/<int:student_id>/', LessonStudentInfoAPIView.as_view(),
         name='lesson_student_info_per_student'),
    path('subjects/',SubjectAPIView.as_view(),name="subjects"),
    path('subjects/<int:subject_id>/',SubjectAPIView.as_view(),name="subject"),
    path('groups/',GroupAPIView.as_view(),name="group"),
    path('groups/<int:group_id>/',GroupAPIView.as_view(),name="group")
]
