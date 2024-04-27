from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
def index(request:HttpRequest)->HttpResponse:
    return render(request,'main/index.html')