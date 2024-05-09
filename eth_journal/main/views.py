from io import StringIO

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404, FileResponse
from main.models import *
from eth_journal.settings import KEY
from cryptography.fernet import Fernet
from datetime import date
from main.forms import ImageForm
import os
import xlsxwriter


def register(request: HttpRequest) -> HttpResponse:
    context = {'error': False}
    if request.method == 'GET':
        return render(request, 'main/register_form.html', context=context)
    if request.user.is_authenticated:
        redirect('main:index')
    login = request.POST.get('login', '').strip()
    while '<' in login:
        login = login.replace('<', '')
    while '>' in login:
        login = login.replace('>', '')
    password = request.POST.get('password', '').strip()
    retype_password = request.POST.get('retype_password', '').strip()
    surname = request.POST.get('surname', '').strip()
    while '<' in surname:
        surname = surname.replace('<', '')
    while '>' in surname:
        surname = surname.replace('>', '')
    name = request.POST.get('name', '').strip()
    while '<' in name:
        name = name.replace('<', '')
    while '>' in name:
        name = name.replace('>', '')

    father_name = request.POST.get('fathname', '').strip()
    while '<' in father_name:
        father_name = father_name.replace('<', '')
    while '>' in father_name:
        father_name = father_name.replace('>', '')

    role = request.POST.get('role', '').strip()
    while '<' in role:
        role = role.replace('<', '')
    while '>' in role:
        role = role.replace('>', '')

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
        while '' in marks:
            marks.remove('')
        while 'УП' in marks:
            marks.remove('УП')
        while 'Н' in marks:
            marks.remove('Н')
        for mark in marks:
            print(mark)
            print(type(mark))
        marks_int = [int(mark) for mark in marks]
        if len(marks_int) != 0:
            avg_mark = str(sum(marks_int) / len(marks_int))
        else:
            avg_mark = str(0)
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
        form = ImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if prev_avatar != 'Empty':
                try:
                    os.remove('media/' + prev_avatar)
                except Exception as e:
                    with open('error.log', 'a') as file:
                        file.write(str(e) + '\n')
            loaded = True
    form = ImageForm()
    context = {"user": request.user, "profile": profile, "my_profile": profile, 'image_form': form, 'loaded': loaded}
    return render(request, 'main/settings.html', context=context)


def admin_requests_view(request: HttpRequest):
    if not request.user.is_superuser:
        raise Http404
    profile = Profile.objects.filter(user=request.user)
    if len(profile) == 0:
        raise Http404
    profile = profile[0]
    groups = Group.objects.all()
    abstract_teachers = AbstractTeacher.objects.all()
    abstract_students = AbstractKid.objects.all()

    context = {'user': request.user, 'my_profile': profile, 'groups': groups, 'abstract_teachers': abstract_teachers,
               'abstract_students': abstract_students}
    return render(request, 'main/admin_requests.html', context=context)


def hours_plan_view(request: HttpRequest):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('get_current_table', None) is not None:
        with open("Hours_Plan.xlsx", "rb") as excel:
            data = excel.read()
            response = HttpResponse(data, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="hours_plan.xlsx"'
            return response

    subject_name = request.GET.get('subject', None)
    group_year_of_study = request.GET.get('group_year_of_study', None)
    group_letter = request.GET.get('group_letter', None)
    if subject_name == "Предмет":
        subject_name = None
    if group_letter == "Буквенный индекс группы":
        group_letter = None
    if group_year_of_study == "Год набора группы":
        group_year_of_study = None
    group = None
    subject = None
    if subject_name is not None:
        subjects = Subject.objects.filter(subject_name=subject_name)
        if len(subjects) != 0:
            subject = subjects[0]
    if group_letter is not None and group_year_of_study is not None:
        groups = Group.objects.filter(year_of_study=int(group_year_of_study), group_letter=group_letter)
        if len(groups) != 0:
            group = groups[0]
    hours_plans = HoursPlan.objects.all()
    if group is not None:
        hours_plans = hours_plans.filter(group=group)
    if subject is not None:
        hours_plans = hours_plans.filter(subject=subject)
    result_array = []
    for hour_plan in hours_plans:
        lessons_count = Lesson.objects.filter(group=hour_plan.group, subject=hour_plan.subject, date__lt=date.today())
        remainder_hours = hour_plan.hours - 2 * len(lessons_count)
        result_array.append({'subject': hour_plan.subject.subject_name,
                             'group': str(hour_plan.group.year_of_study) + hour_plan.group.group_letter,
                             'remainder': remainder_hours, 'planned': hour_plan.hours})
    profile = Profile.objects.filter(user=request.user)
    if len(profile) == 0:
        raise Http404
    profile = profile[0]
    all_groups = Group.objects.all()
    all_subjects = Subject.objects.all()
    all_groups_years = [group.year_of_study for group in all_groups]
    all_groups_letters = [group.group_letter for group in all_groups]
    all_subjects_names = [subject.subject_name for subject in all_subjects]

    workbook = xlsxwriter.Workbook('Hours_Plan.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    # Заголовок таблицы
    worksheet.write(row, col, 'Предмет')
    worksheet.write(row, col + 1, 'Группа')
    worksheet.write(row, col + 2, 'Запланированно часов')
    worksheet.write(row, col + 3, 'Осталось часов')

    row += 1
    for result in result_array:
        worksheet.write(row, col, result['subject'])
        worksheet.write(row, col + 1, result['group'])
        worksheet.write(row, col + 2, result['planned'])
        worksheet.write(row, col + 3, result['remainder'])
        row += 1
    workbook.close()

    context = {'result_array': result_array, 'my_profile': profile,
               'all_subjects_names': all_subjects_names, 'all_groups_letters': all_groups_letters,
               'all_groups_years': all_groups_years}
    return render(request, 'main/hours_plan.html', context=context)


def raiting(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404
    profile = Profile.objects.filter(user=request.user)
    if len(profile) == 0:
        raise Http404
    profile = profile[0]
    context = {'my_profile':profile}
    return render(request, 'main/raiting.html', context=context)
