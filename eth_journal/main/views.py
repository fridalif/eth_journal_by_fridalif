from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404

# Create your views here.
def index(request:HttpRequest)->HttpResponse:
    return render(request,'main/index.html')