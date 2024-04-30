from rest_framework.serializers import ModelSerializer
from main.models import Lesson, LessonStudentInfo, Subject, Kid, Teacher, Group


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonStudentInfoSerializer(ModelSerializer):
    class Meta:
        model = LessonStudentInfo
        fields = '__all__'


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class KidSerializer(ModelSerializer):
    class Meta:
        model = Kid
        fields = '__all__'


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
