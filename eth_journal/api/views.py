from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpRequest, Http404
from .serializers import RegisterRequestsSerializer, TeacherSerializer, KidSerializer, LessonSerializer, \
    LessonStudentInfoSerializer
import main.models as main_models
from eth_journal.settings import KEY
from cryptography.fernet import Fernet


class RegisterRequestsAPIView(APIView):
    def get(self, request: HttpRequest):
        if not request.user.is_superuser:
            raise Http404
        return Response(RegisterRequestsSerializer(main_models.RegisterRequests.objects.all(), many=True).data)

    def post(self, request):
        data = request.data
        if not request.user.is_superuser:
            raise Http404

        if not data['id']:
            raise Http404

        current_request = main_models.RegisterRequests.objects.filter(id=int(data['id']))
        if len(current_request) == 0:
            raise Http404
        current_request = current_request[0]

        cipher_suite = Fernet(KEY)
        password = cipher_suite.decrypt(current_request.password.encode()).decode()
        if data['role'] == 'Teacher':
            current_user = main_models.User(username=current_request.login,
                                            first_name=current_request.name, last_name=current_request.surname)
            current_user.set_password(password)
            current_user.save()
            current_teacher = main_models.Teacher(user=current_user, father_name=current_request.father_name)
            current_teacher.save()
            abstract_teacher_id = int(data['abstract_id'])
            abstract_teacher = main_models.AbstractTeacher.objects.filter(id=abstract_teacher_id)
            if len(abstract_teacher) != 0:
                abstract_teacher = abstract_teacher[0]
                abstract_teacher_lessons = main_models.Lesson.objects.filter(abstract_teacher=abstract_teacher)
                for lesson in abstract_teacher_lessons:
                    lesson.teacher = current_teacher
                abstract_teacher.delete()
            current_request.delete()
            return Response(TeacherSerializer(current_teacher).data)

        if data['role'] == 'Student':
            current_group = main_models.Group.objects.filter(id=int(data['group']))
            if len(current_request) == 0:
                raise Http404
            current_group = current_group[0]

            current_user = main_models.User(username=current_request.login,
                                            first_name=current_request.name, last_name=current_request.surname)
            current_user.set_password(password)
            current_user.save()

            current_student = main_models.Kid(user=current_user, group=current_group,
                                              father_name=current_request.father_name)

            abstract_student_id = int(data['abstract_id'])
            abstract_student = main_models.AbstractTeacher.objects.filter(id=abstract_student_id)
            if len(abstract_student) != 0:
                abstract_student = abstract_student[0]
                abstract_student_lessons_info = main_models.LessonStudentInfo.objects.filter(
                    abstract_student=abstract_student)
                for lesson_info in abstract_student_lessons_info:
                    lesson_info.student = current_student
                abstract_student.delete()

            current_student.save()
            current_request.delete()
            return Response(KidSerializer(current_student).data)
        raise Http404

    def delete(self, request):
        data = request.data
        if not request.user.is_superuser:
            raise Http404

        if not data['id']:
            raise Http404

        current_request = main_models.RegisterRequests.objects.filter(id=int(data['id']))
        if len(current_request) == 0:
            raise Http404
        current_request = current_request[0]
        current_request.delete()
        return Response({"result": "deleted"})


class LessonAPIView(APIView):
    def get(self, request, lesson_id=None):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_superuser:
            if lesson_id is not None:
                lesson = main_models.Lesson.objects.filter(id=lesson_id)
                if len(lesson) == 0:
                    raise Http404
                return Response(LessonSerializer(lesson[0]).data)
            return Response(LessonSerializer(main_models.Lesson.objects.all(), many=True).data)

        teacher = main_models.Teacher.objects.filter(user=request.user)
        student = main_models.Kid.objects.filter(user=request.user)
        is_student = False
        if len(teacher) == 0 and len(student) == 0:
            raise Http404
        if len(student) == 0:
            teacher = teacher[0]
        else:
            student = student[0]
            is_student = True
        if not is_student:
            if lesson_id is not None:
                lesson = main_models.Lesson.objects.filter(teacher=teacher, id=lesson_id)
                if len(lesson):
                    raise Http404
                return Response(LessonSerializer(lesson[0]).data)
            return Response(LessonSerializer(main_models.Lesson.objects.filter(teacher=teacher), many=True).data)
        if lesson_id is not None:
            lesson = main_models.Lesson.objects.filter(group=student.group, id=lesson_id)
            if len(lesson) == 0:
                raise Http404
            return Response(LessonSerializer(lesson[0]).data)
        return Response(LessonSerializer(main_models.Lesson.objects.filter(group=student.group), many=True).data)

    def post(self, request):
        if not request.user.is_superuser:
            raise Http404
        lesson = LessonSerializer(data=request.data)
        if lesson.is_valid():
            lesson.save()
            return Response(lesson.validated_data)
        return Response({'error': 'lesson is not valid'})

    def put(self, request: HttpRequest, lesson_id=None):
        data = request.data
        lesson = main_models.Lesson.objects.filter(id=lesson_id)
        if len(lesson) == 0:
            raise Http404
        lesson = lesson[0]

        if request.user.is_superuser:
            group = main_models.Group.objects.filter(id=int(data['group']))
            teacher = main_models.Teacher.objects.filter(id=int(data['teacher']))
            subject = main_models.Subject.objects.filter(id=int(data['subject']))
            if len(group) == 0 or len(teacher) == 0 or len(subject) == 0:
                return Response({'error': 'lesson is not valid'})
            group = group[0]
            teacher = teacher[0]
            subject = subject[0]
            lesson.group = group
            lesson.subject = subject
            lesson.teacher = teacher
            lesson.date = data['date']
            lesson.start_time = data['start_time']
            lesson.end_time = data['end_time']
            lesson.homework = data['homework']
            lesson.room = data['room']
            lesson.type = data['type']
            lesson.save()
            return Response(LessonSerializer(lesson).data)
        if lesson.teacher.user == request.user:
            lesson.homework = data['homework']
            lesson.room = data['room']
            lesson.save()
            return Response(LessonSerializer(lesson).data)
        raise Http404

    def delete(self, request, lesson_id):
        if not request.user.is_superuser:
            raise Http404
        lesson = main_models.Lesson.objects.filter(id=lesson_id)
        if len(lesson) == 0:
            raise Http404
        lesson[0].delete()
        return Response({"result": "deleted"})


class LessonStudentInfoAPIView(APIView):
    def get(self, request, lesson_id=None, student_id=None):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_superuser:
            if lesson_id is None and student_id is None:
                return Response(
                    LessonStudentInfoSerializer(main_models.LessonStudentInfo.objects.all(), many=True).data)
            if student_id is None:
                return Response(
                    LessonStudentInfoSerializer(main_models.LessonStudentInfo.objects.filter(lesson__id=lesson_id),
                                                many=True).data)

            if not request.GET['abstract']:
                return Response(LessonStudentInfoSerializer(
                    main_models.LessonStudentInfo.objects.filter(lesson__id=lesson_id, student__id=student_id),
                    many=True).data)
            return Response(LessonStudentInfoSerializer(
                main_models.LessonStudentInfo.objects.filter(lesson__id=lesson_id, abstract_studenet__id=student_id),
                many=True).data)
