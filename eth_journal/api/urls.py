from django.urls import path, include
from .views import RegisterRequestsAPIView, LessonAPIView, LessonStudentInfoAPIView, SubjectAPIView, GroupAPIView, \
    AbstractKidAPIView, AbstractTeacherAPIView, ProfileRaitingAPIView, ChangePasswordAPIView

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
    path('subjects/', SubjectAPIView.as_view(), name="subjects"),
    path('subjects/<int:subject_id>/', SubjectAPIView.as_view(), name="subject"),
    path('groups/', GroupAPIView.as_view(), name="groups"),
    path('groups/<int:group_id>/', GroupAPIView.as_view(), name="group"),
    path('abstract_kids/', AbstractKidAPIView.as_view(), name="abstract_kids"),
    path('abstract_kids/<int:student_id>/', AbstractKidAPIView.as_view(), name="abstract_kid"),
    path('abstract_teachers/', AbstractTeacherAPIView.as_view(), name="abstract_teachers"),
    path('abstract_teachers/<int:teacher_id>/', AbstractTeacherAPIView.as_view(), name="abstract_teacher"),
    path('profile_raiting/<slug:profile_slug>/', ProfileRaitingAPIView.as_view(), name='profile_raiting'),
    path('change_password/<int:request_id>/',ChangePasswordAPIView.as_view(),name='change_password_request'),
    path('change_password/',ChangePasswordAPIView.as_view(),name='change_password_requests')
]
