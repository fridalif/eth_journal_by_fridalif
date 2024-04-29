from django.contrib import admin
from .models import Lesson,LessonStudentInfo,Subject,Kid,Teacher,Group,RegisterRequests


# Register your models here.
admin.site.register(Lesson)
admin.site.register(LessonStudentInfo)
admin.site.register(Subject)
admin.site.register(Kid)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(RegisterRequests)
