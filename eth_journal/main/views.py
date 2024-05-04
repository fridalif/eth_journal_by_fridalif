from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from .models import *
from eth_journal.settings import KEY
from cryptography.fernet import Fernet
from datetime import date


def register(request: HttpRequest) -> HttpResponse:
    context = {'error': False}
    if request.method == 'GET':
        return render(request, 'main/register_form.html', context=context)
    if request.user.is_authenticated:
        redirect('main:index')
    login = request.POST['login'].strip()
    password = request.POST['password'].strip()
    retype_password = request.POST['retype_password'].strip()
    surname = request.POST['surname'].strip()
    name = request.POST['name'].strip()
    father_name = request.POST['fathname'].strip()
    role = request.POST['role'].strip()

    # Валидация
    if login == '' or password == '' or retype_password == '' or surname == '' or name == '' or role == '':
        context['error'] = 'Пожалуйста, заполните все обязательные поля(отчество, если имеете)'
        return render(request, 'main/register_form.html', context=context)
    if retype_password != password:
        context['error'] = 'Поля Пароль и Повторите пароль должны совпадать'
        return render(request, 'main/register_form.html', context=context)
    if len(User.objects.filter(username=login)) != 0 or len(RegisterRequests.objects.filter(login=login)) != 0:
        context['error'] = 'Пользователь с таким Логином уже существует.'
        return render(request, 'main/register_form.html', context=context)

    # Шифрование пароля(чтобы не хранить в открытом виде в БД) и создание записи в БД
    cipher_suite = Fernet(KEY)
    password = cipher_suite.encrypt(password.encode()).decode()
    register_request = RegisterRequests(login=login, password=password, surname=surname, name=name,
                                        father_name=father_name, role=role)
    register_request.save()
    context['error'] = 'Ваш запрос на регистрацию был отправлен на рассмотрение администратору.'
    return render(request, 'main/register_form.html', context=context)


def index(request: HttpRequest) -> HttpResponse:
    my_profile = Profile.objects.filter(user=request.user)
    if len(my_profile) == 0 and request.user.is_authenticated:
        raise Http404
    my_profile = my_profile[0]
    context = {'user': request.user,'my_profile':my_profile}
    return render(request, 'main/index.html', context=context)


def lessons_plan(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('main:login')
    is_teacher = False
    if request.user.is_authenticated:
        if request.user.is_superuser:
            is_teacher = True
        if len(Teacher.objects.filter(user=request.user)) != 0:
            is_teacher = True
    my_profile = Profile.objects.filter(user=request.user)
    if len(my_profile) == 0:
        raise Http404
    my_profile = my_profile[0]
    today = date.today()
    context = {"user": request.user, "day": today.day, "month": today.month, "year": today.year,
               "is_teacher": is_teacher, "my_profile": my_profile}
    return render(request, 'main/lesson_plan.html', context=context)


def profile(request: HttpRequest, profile_slug) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('main:login')
    my_profile = Profile.objects.filter(user=request.user)
    profile = Profile.objects.filter(slug=profile_slug)
    if len(my_profile) == 0 or len(profile) == 0:
        raise Http404
    my_profile = my_profile[0]
    profile = profile[0]
    context = {"user": request.user, "my_profile": my_profile, "profile":profile}
    return render(request, 'main/profile.html', context=context)
