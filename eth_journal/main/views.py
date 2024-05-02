from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import *
from eth_journal.settings import KEY
from cryptography.fernet import Fernet
from datetime import date


def register(request: HttpRequest) -> HttpResponse:
    context = {'error': False}
    if request.method == 'GET':
        return render(request, 'main/register_form.html', context=context)

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
    context = {'user': request.user}
    return render(request, 'main/index.html', context=context)


def lessons_plan(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('main:login')
    today = date.today()
    context = {"user": request.user, "day": today.day, "month": today.month, "year": today.year}
    return render(request, 'main/lesson_plan.html', context=context)
