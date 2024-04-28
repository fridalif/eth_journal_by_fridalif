from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import KidSerializer
from .models import *


class StudentsAPIView(APIView):
    def get(self, request: HttpRequest) -> Response:
        return Response(KidSerializer(Kid.objects.all(), many=True).data)


class TestAuthAPIView(APIView):
    def get(self, request: HttpRequest) -> Response:
        auth = request.user.is_authenticated
        print(auth)
        return Response({'res': auth})


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/index.html')


#def login(request: HttpRequest) -> HttpResponse:
#    return render(request, 'main/login.html')
