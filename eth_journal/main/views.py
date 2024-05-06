from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from main.models import *
from eth_journal.settings import KEY
from cryptography.fernet import Fernet
from datetime import date
from main.forms import ImageForm
import os

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
    if request.user.is_authenticated:
        my_profile = Profile.objects.filter(user=request.user)
        if len(my_profile) == 0:
            raise Http404
        my_profile = my_profile[0]
    else:
        my_profile = None
    context = {'user': request.user, 'my_profile': my_profile}
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
    student = Kid.objects.filter(user=profile.user)
    avg_mark = 'Не студент'
    if len(student) != 0:
        student = student[0]
        lessons_info = LessonStudentInfo.objects.filter(student=student)
        marks = [lesson_info.mark for lesson_info in lessons_info]
        if '' in marks:
            marks.remove('')
        if 'УП' in marks:
            marks.remove('УП')
        if 'Н' in marks:
            marks.remove('Н')
        marks_int = [int(mark) for mark in marks]
        avg_mark = str(sum(marks_int) / len(marks_int))
    carma = ProfileRaiting.objects.filter(profile=profile)
    carma_percentage = '100%'
    if len(carma) != 0:
        carma_percentage = str(
            (len(ProfileRaiting.objects.filter(profile=profile, like=True)) / len(carma)) * 100) + '%'
    context = {"user": request.user, "my_profile": my_profile, "profile": profile, "avg_mark": avg_mark,
               "carma_count": len(carma), "carma_percentage": carma_percentage}
    return render(request, 'main/profile.html', context=context)


def settings(request):
    if not request.user.is_authenticated:
        return redirect('main:login')
    profile = Profile.objects.filter(user=request.user)
    if len(profile) == 0:
        raise Http404
    profile = profile[0]
    loaded = False
    if request.method == 'POST':
        prev_avatar = profile.avatar.name
        form = ImageForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            if prev_avatar is not None:
                try:
                    os.remove('media/'+prev_avatar)
                except Exception as e:
                    with open('error.log','a') as file:
                        file.write(str(e))
            loaded = True
    form = ImageForm()
    context = {"user": request.user, "profile": profile, "my_profile": profile, 'image_form': form, 'loaded': loaded}
    return render(request, 'main/settings.html', context=context)
