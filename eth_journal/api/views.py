from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpRequest, Http404
from .serializers import RegisterRequestsSerializer, TeacherSerializer, KidSerializer
import main.models as main_models
from eth_journal.settings import KEY
from cryptography.fernet import Fernet


class RegisterRequestsAPIView(APIView):
    def get(self, request: HttpRequest):
        if not request.user.is_superuser:
            raise Http404
        return Response(RegisterRequestsSerializer(main_models.RegisterRequests.objects.all(), many=True).data)

    def post(self, request: HttpRequest):
        if not request.user.is_superuser:
            raise Http404

        if not request.POST['id']:
            raise Http404

        current_request = main_models.RegisterRequests.objects.get(id=int(request.POST['id']))
        if current_request is None:
            raise Http404

        cipher_suite = Fernet(KEY)
        password = cipher_suite.decrypt(current_request.password).decode()
        if request.POST['role'] == 'Teacher':
            current_user = main_models.User(username=current_request.login, password=password,
                                            first_name=current_request.name, last_name=current_request.surname)
            current_user.save()
            current_teacher = main_models.Teacher(user=current_user, father_name=current_request.father_name)
            current_teacher.save()
            return Response(TeacherSerializer(current_teacher).data)

        if request.POST['role'] == 'Student':
            current_group = main_models.Group.objects.get(id=int(request.POST['group']))
            if current_group is None:
                raise Http404
            current_user = main_models.User(username=current_request.login, password=password,
                                            first_name=current_request.name, last_name=current_request.surname)
            current_user.save()
            current_student = main_models.Kid(user=current_user, group=current_group,
                                              father_name=current_request.father_name)
            current_student.save()
            return Response(KidSerializer(current_student).data)
        raise Http404
