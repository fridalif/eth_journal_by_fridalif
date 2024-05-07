from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpRequest, Http404
from .serializers import RegisterRequestsSerializer, TeacherSerializer, KidSerializer, LessonSerializer, \
    LessonStudentInfoSerializer, SubjectSerializer, GroupSerializer, AbstractKidSerializer, AbstractTeacherSerializer, \
    ChangePasswordRequestsSerializer
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
            user_profile = main_models.Profile(user=current_user, slugify='not important')
            user_profile.save()
            abstract_teacher_id = data.get('abstract_id', None)
            if abstract_teacher_id is not None:
                abstract_teacher_id = int(abstract_teacher_id)
            if abstract_teacher_id is not None:
                abstract_teacher = main_models.AbstractTeacher.objects.filter(id=abstract_teacher_id)
            else:
                abstract_teacher = []
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
            user_profile = main_models.Profile(user=current_user, slugify='not important')
            user_profile.save()
            current_student = main_models.Kid(user=current_user, group=current_group,
                                              father_name=current_request.father_name)

            abstract_student_id = data.get('abstract_id', None)
            if abstract_student_id is not None:
                abstract_student_id = int(abstract_student_id)
            if abstract_student_id is not None:
                abstract_student = main_models.AbstractKid.objects.filter(id=abstract_student_id)
            else:
                abstract_student = []
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
        date = request.GET.get('date', None)
        if request.user.is_superuser:
            if lesson_id is not None:
                lesson = main_models.Lesson.objects.filter(id=lesson_id)
                if len(lesson) == 0:
                    raise Http404
                return Response(LessonSerializer(lesson[0]).data)
            if date is not None:
                return Response(LessonSerializer(main_models.Lesson.objects.filter(date=date), many=True).data)
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
            if date is not None:
                return Response(
                    LessonSerializer(main_models.Lesson.objects.filter(teacher=teacher, date=date), many=True).data)
            return Response(LessonSerializer(main_models.Lesson.objects.filter(teacher=teacher), many=True).data)
        if lesson_id is not None:
            lesson = main_models.Lesson.objects.filter(group=student.group, id=lesson_id)
            if len(lesson) == 0:
                raise Http404
            return Response(LessonSerializer(lesson[0]).data)
        if date is not None:
            return Response(
                LessonSerializer(main_models.Lesson.objects.filter(group=student.group, date=date), many=True).data)
        return Response(LessonSerializer(main_models.Lesson.objects.filter(group=student.group), many=True).data)

    def post(self, request):
        if not request.user.is_superuser:
            raise Http404
        data = request.data
        lesson = main_models.Lesson()
        lesson.date = data['date']
        lesson.start_time = data['start_time']
        lesson.end_time = data['end_time']
        lesson.type = data['type']
        lesson.homework = data['homework']
        lesson.room = data['room']
        group = main_models.Group.objects.filter(id=data['group'])
        subject = main_models.Subject.objects.filter(id=data['subject'])
        if len(group) == 0 or len(subject) == 0:
            return Response({"error": 'group or subject dosnt exists'})
        group = group[0]
        subject = subject[0]
        lesson.group = group
        lesson.subject = subject
        teacher = data.get('teacher', None)
        abstract_teacher = data.get('abstract_teacher', None)
        if abstract_teacher is None and teacher is None:
            return Response({"error": 'teacher dosnt exists'})
        if teacher is not None:
            teacher = main_models.Teacher.objects.filter(id=teacher)
            if len(teacher) == 0:
                return Response({"error": 'teacher dosnt exists'})
            lesson.teacher = teacher[0]
        else:
            abstract_teacher = main_models.AbstractTeacher.objects.filter(id=abstract_teacher)
            if len(abstract_teacher) == 0:
                return Response({"error": 'abstract_teacher dosnt exists'})
            lesson.abstract_teacher = abstract_teacher[0]
        lesson.save()
        group = lesson.group
        students = main_models.Kid.objects.filter(group=group)
        abstract_students = main_models.AbstractKid.objects.filter(group=group)
        for student in students:
            lesson_student_info = main_models.LessonStudentInfo(lesson=lesson, student=student)
            lesson_student_info.save()
        for abstract_student in abstract_students:
            lesson_student_info = main_models.LessonStudentInfo(lesson=lesson, abstract_student=abstract_student)
            lesson_student_info.save()
        return Response(LessonSerializer(lesson).data)

    def put(self, request: HttpRequest, lesson_id):
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
        current_user = request.user
        is_student = False
        current_teacher = main_models.Teacher.objects.filter(user=current_user)
        current_student = main_models.Kid.objects.filter(user=current_user)
        if len(current_teacher) == 0:
            is_student = True
            current_student = current_student[0]
        else:
            current_teacher = current_teacher[0]

        if is_student:
            if lesson_id is None:
                return Response(
                    LessonStudentInfoSerializer(main_models.LessonStudentInfo.objects.filter(student=current_student),
                                                many=True).data)
            return Response(
                LessonStudentInfoSerializer(
                    main_models.LessonStudentInfo.objects.filter(student=current_student, lesson__id=lesson_id),
                    many=True).data)
        if lesson_id is None:
            return Response(LessonStudentInfoSerializer(
                main_models.LessonStudentInfo.objects.filter(lesson__teacher=current_teacher), many=True).data)
        if student_id is None:
            return Response(LessonStudentInfoSerializer(
                main_models.LessonStudentInfo.objects.filter(lesson__teacher=current_teacher, lesson__id=lesson_id),
                many=True).data)
        if not request.GET['abstract']:
            return Response(
                LessonStudentInfoSerializer(
                    main_models.LessonStudentInfo.objects.filter(lesson__teacher=current_teacher, lesson__id=lesson_id,
                                                                 student__id=student_id),
                    many=True).data)
        return Response(
            LessonStudentInfoSerializer(
                main_models.LessonStudentInfo.objects.filter(lesson__teacher=current_teacher, lesson__id=lesson_id,
                                                             abstract_student__id=student_id),
                many=True).data)

    def post(self, request, lesson_id, student_id):
        data = request.data
        if not request.user.is_superuser and len(
                main_models.Lesson.objects.filter(teacher__user=request.user, id=lesson_id)) == 0:
            raise Http404
        lesson = main_models.Lesson.objects.filter(id=lesson_id)[0]
        if data['abstract']:
            student = main_models.AbstractKid.objects.filter(id=student_id)
            if len(student) == 0:
                raise Http404
            student = student[0]
            if len(main_models.LessonStudentInfo.objects.filter(abstract_student=student, lesson=lesson)) != 0:
                return Response({"error": "this student alredy has info in this lesson"})
            lesson_student_info = main_models.LessonStudentInfo(student=None, abstract_student=student, lesson=lesson,
                                                                mark=data['mark'], commendation=data['commendation'],
                                                                chastisement=data['chastisement'])
            lesson_student_info.save()
            return Response(LessonStudentInfoSerializer(lesson_student_info).data)
        student = main_models.Kid.objects.filter(id=student_id)
        if len(student) == 0:
            raise Http404
        student = student[0]
        if len(main_models.LessonStudentInfo.objects.filter(student=student, lesson=lesson)) != 0:
            return Response({"error": "this student alredy has info in this lesson"})
        lesson_student_info = main_models.LessonStudentInfo(student=student, abstract_student=None, lesson=lesson,
                                                            mark=data['mark'], commendation=data['commendation'],
                                                            chastisement=data['chastisement'])
        lesson_student_info.save()
        return Response(LessonStudentInfoSerializer(lesson_student_info).data)

    def put(self, request, lesson_id):
        data = request.data
        if not request.user.is_superuser and len(
                main_models.Lesson.objects.filter(teacher__user=request.user, id=lesson_id)) == 0:
            raise Http404
        lesson = main_models.Lesson.objects.filter(id=lesson_id)
        if len(lesson) == 0:
            raise Http404
        lesson = lesson[0]
        lesson_student_info = main_models.LessonStudentInfo.objects.filter(id=int(data['id']), lesson=lesson)
        if len(lesson_student_info) == 0:
            raise Http404
        lesson_student_info = lesson_student_info[0]
        lesson_student_info.mark = data['mark']
        lesson_student_info.commendation = data['commendation']
        lesson_student_info.chastisement = data['chastisement']
        lesson_student_info.save()
        return Response(LessonStudentInfoSerializer(lesson_student_info).data)


class SubjectAPIView(APIView):
    def get(self, request, subject_id=None):
        if not request.user.is_authenticated:
            return Response({"error": "not authenticated"})
        if subject_id is None:
            return Response(SubjectSerializer(main_models.Subject.objects.all(), many=True))
        return Response(SubjectSerializer(main_models.Subject.objects.filter(id=subject_id), many=True))

    def post(self, request):
        if not request.user.is_superuser:
            raise Http404
        subject = SubjectSerializer(data=request.data)
        if subject.is_valid():
            subject.save()
            return Response(subject.validated_data)
        return Response({"error": "subject not valid"})

    def put(self, request, subject_id):
        if not request.user.is_superuser:
            raise Http404
        subject = main_models.Subject.objects.filter(id=subject_id)
        if len(subject) == 0:
            raise Http404
        subject[0].subject_name = request.data['subject_name']
        subject[0].save()
        return Response(SubjectSerializer(subject[0]).data)

    def delete(self, request, subject_id):
        if not request.user.is_superuser:
            raise Http404
        subject = main_models.Subject.objects.filter(id=subject_id)
        if len(subject) == 0:
            raise Http404
        subject[0].delete()
        return Response({"result": "deleted"})


class GroupAPIView(APIView):
    def get(self, request, group_id=None):
        if not request.user.is_authenticated:
            return Response({"error": "not authenticated"})
        if group_id is None:
            return Response(GroupSerializer(main_models.Group.objects.all(), many=True))
        return Response(GroupSerializer(main_models.Group.objects.filter(id=group_id), many=True))

    def post(self, request):
        if not request.user.is_superuser:
            raise Http404
        group = GroupSerializer(data=request.data)
        if group.is_valid():
            group.save()
            return Response(group.validated_data)
        return Response({"error": "group not valid"})

    def put(self, request, group_id):
        if not request.user.is_superuser:
            raise Http404
        group = main_models.Group.objects.filter(id=group_id)
        if len(group) == 0:
            raise Http404
        group[0].year_of_study = request.data['year_of_study']
        group[0].group_letter = request.data['group_letter']
        group[0].save()
        return Response(GroupSerializer(group[0]).data)

    def delete(self, request, group_id):
        if not request.user.is_superuser:
            raise Http404
        group = main_models.Group.objects.filter(id=group_id)
        if len(group) == 0:
            raise Http404
        group[0].delete()
        return Response({"result": "deleted"})


class AbstractKidAPIView(APIView):
    def get(self, request, student_id=None):
        if not request.user.is_superuser:
            raise Http404
        if student_id is None:
            return Response(AbstractKidSerializer(main_models.AbstractKid.objects.all(), many=True))
        return Response(AbstractKidSerializer(main_models.AbstractKid.objects.filter(id=student_id), many=True))

    def post(self, request):
        if not request.user.is_superuser:
            raise Http404
        abstract_kid = AbstractKidSerializer(data=request.data)
        if abstract_kid.is_valid():
            abstract_kid.save()
            return Response(abstract_kid.validated_data)
        return Response({"error": "abstract kid not valid"})

    def put(self, request, student_id):
        if not request.user.is_superuser:
            raise Http404
        abstract_kid = main_models.AbstractKid.objects.filter(id=student_id)
        if len(abstract_kid) == 0:
            raise Http404
        abstract_kid = abstract_kid[0]
        abstract_kid['name'] = request.data['name']
        abstract_kid['surname'] = request.data['surname']
        abstract_kid['father_name'] = request.data['father_name']
        group = main_models.Group.objects.filter(id=int(request.data['group_id']))
        if len(group) == 0:
            return Response({"error": "Group not found"})
        abstract_kid.group = group[0]
        abstract_kid.save()
        return Response(AbstractKidSerializer(abstract_kid).data)

    def delete(self, request, student_id):
        if not request.user.is_superuser:
            raise Http404
        abstract_kid = main_models.AbstractKid.objects.filter(id=student_id)
        if len(abstract_kid) == 0:
            raise Http404
        abstract_kid[0].delete()
        return Response({"result": "deleted"})


class AbstractTeacherAPIView(APIView):
    def get(self, request, teacher_id=None):
        if not request.user.is_superuser:
            raise Http404
        if teacher_id is None:
            return Response(AbstractTeacherSerializer(main_models.AbstractTeacher.objects.all(), many=True))
        return Response(AbstractTeacherSerializer(main_models.AbstractTeacher.objects.filter(id=teacher_id), many=True))

    def post(self, request):
        if not request.user.is_superuser:
            raise Http404
        abstract_teacher = AbstractTeacherSerializer(data=request.data)
        if abstract_teacher.is_valid():
            abstract_teacher.save()
            return Response(abstract_teacher.validated_data)
        return Response({"error": "abstract teacher not valid"})

    def put(self, request, teacher_id):
        if not request.user.is_superuser:
            raise Http404
        abstract_teacher = main_models.AbstractTeacher.objects.filter(id=teacher_id)
        if len(abstract_teacher) == 0:
            raise Http404
        abstract_teacher = abstract_teacher[0]
        abstract_teacher['name'] = request.data['name']
        abstract_teacher['surname'] = request.data['surname']
        abstract_teacher['father_name'] = request.data['father_name']
        abstract_teacher.save()
        return Response(AbstractTeacherSerializer(abstract_teacher).data)

    def delete(self, request, teacher_id):
        if not request.user.is_superuser:
            raise Http404
        abstract_teacher = main_models.AbstractTeacher.objects.filter(id=teacher_id)
        if len(abstract_teacher) == 0:
            raise Http404
        abstract_teacher[0].delete()
        return Response({"result": "deleted"})


class ProfileRaitingAPIView(APIView):
    def post(self, request, profile_slug):
        data = request.data
        if not request.user.is_authenticated:
            raise Http404
        profile = main_models.Profile.objects.filter(slug=profile_slug)
        if len(profile) == 0:
            raise Http404
        profile = profile[0]
        profile_raiting_from_this_user = main_models.ProfileRaiting.objects.filter(from_user=request.user,
                                                                                   profile=profile)
        if len(profile_raiting_from_this_user) != 0:
            profile_raiting_from_this_user = profile_raiting_from_this_user[0]
            if data['send_type'] == 'like':
                profile_raiting_from_this_user.like = True
                profile_raiting_from_this_user.dislike = False
            else:
                profile_raiting_from_this_user.like = False
                profile_raiting_from_this_user.dislike = True
            profile_raiting_from_this_user.save()
            carma = main_models.ProfileRaiting.objects.filter(profile=profile)
            carma_percentage = '100%'
            if len(carma) != 0:
                carma_percentage = str(
                    (len(main_models.ProfileRaiting.objects.filter(profile=profile, like=True)) / len(
                        carma)) * 100) + '%'
            return Response({"response": "Успешно!", "carma_count": len(carma), "carma_percentage": carma_percentage})
        new_vote = main_models.ProfileRaiting()
        new_vote.profile = profile
        new_vote.from_user = request.user
        if data['send_type'] == 'like':
            new_vote.like = True
            new_vote.dislike = False
            new_vote.save()
            carma = main_models.ProfileRaiting.objects.filter(profile=profile)
            carma_percentage = '100%'
            if len(carma) != 0:
                carma_percentage = str(
                    (len(main_models.ProfileRaiting.objects.filter(profile=profile, like=True)) / len(
                        carma)) * 100) + '%'
            return Response({"response": "Успешно!", "carma_count": len(carma), "carma_percentage": carma_percentage})
        new_vote.like = False
        new_vote.dislike = True
        new_vote.save()
        carma = main_models.ProfileRaiting.objects.filter(profile=profile)
        carma_percentage = '100%'
        if len(carma) != 0:
            carma_percentage = str(
                (len(main_models.ProfileRaiting.objects.filter(profile=profile, like=True)) / len(carma)) * 100) + '%'
        return Response({"response": "Успешно!", "carma_count": len(carma), "carma_percentage": carma_percentage})


class ChangePasswordAPIView(APIView):
    def get(self, request, request_id=None):
        if not request.user.is_superuser:
            raise Http404
        if request_id is None:
            return Response(
                ChangePasswordRequestsSerializer(main_models.ChangePasswordRequests.objects.all(), many=True).data)
        return Response(
            ChangePasswordRequestsSerializer(main_models.ChangePasswordRequests.objects.filter(id=request_id),
                                             many=True).data)

    def post(self, request):
        data = request.data
        prev_password = data.get('prev_password', None)
        new_password = data.get('new_password', None)
        other_data = data.get('other_data', None)
        user_id = data.get('user', None)
        user_to_change_password = main_models.User.objects.filter(id=user_id)
        if len(user_to_change_password) == 0:
            raise Http404
        user_to_change_password = user_to_change_password[0]
        if request.user.is_authenticated and request.user != user_to_change_password:
            raise Http404
        if not user_to_change_password.check_password(prev_password) and prev_password is not None:
            print(prev_password)
            return Response({'error': 'Прошлый пароль введён неверно'})
        if new_password.strip() == '' or new_password is None:
            return Response({'error': 'Пароль не может быть пустым'})
        new_request = main_models.ChangePasswordRequests()
        new_request.user = user_to_change_password
        cipher_suite = Fernet(KEY)
        new_request.new_password = cipher_suite.encrypt(new_password.encode()).decode()
        if user_to_change_password.check_password(prev_password):
            new_request.know_previous_password = True
        else:
            new_request.know_previous_password = False

        if request.user.is_authenticated:
            new_request.other_info = 'Вход в аккаунт был совершён: Да.'
        else:
            new_request.other_info = 'Вход в аккаунт был совершён: Нет.'
        new_request.other_info += str(other_data)
        new_request.save()
        return Response({'result': 'Запрос на смену пароля отправлен администратору!'})

    def put(self, request, request_id):
        if not request.user.is_superuser:
            raise Http404
        current_request = main_models.ChangePasswordRequests.objects.filter(id=request_id)
        if len(current_request) == 0:
            raise Http404
        current_request = current_request[0]
        user = current_request.user
        cipher_suite = Fernet(KEY)
        new_password = cipher_suite.decrypt(current_request.new_password.encode()).decode()
        user.set_password(new_password)
        current_request.delete()
        return Response({'result': 'password changed'})

    def delete(self, request, request_id):
        if not request.user.is_superuser:
            raise Http404
        current_request = main_models.ChangePasswordRequests.objects.filter(id=request_id)
        if len(current_request) == 0:
            raise Http404
        current_request = current_request[0]
        current_request.delete()
        return Response({'result': 'deleted'})


class ChangeUsernameAPIView(APIView):
    def post(self, request):
        data = request.data
        new_username = data.get('new_username', None)
        if new_username is None:
            return Response({'error': 'Логин не может быть пустым'})
        new_username = new_username.strip()
        if new_username.strip() == '':
            return Response({'error': 'Логин не может быть пустым'})
        if len(main_models.User.objects.filter(username=new_username)) != 0:
            return Response({'error': 'Логин занят'})
        user = request.user
        user.username = new_username
        user.save()
        return Response({'result': 'Логин успешно изменён!'})
