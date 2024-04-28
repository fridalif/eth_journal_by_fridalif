from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    year_of_study = models.IntegerField(verbose_name='Год набора')
    group_letter = models.CharField(max_length=2, verbose_name='Буквенный индекс группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Kid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь в системе')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    father_name = models.TextField(verbose_name='Отчество', blank=True)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Subject(models.Model):
    subject_name = models.TextField(verbose_name='Название предмета')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь в системе')
    father_name = models.TextField(verbose_name='Отчество', blank=True)
    room = models.CharField(max_length=10, verbose_name='Рабочий кабинет', blank=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    homework = models.TextField(verbose_name='Домашнее задание', blank=True)
    room = models.CharField(max_length=10, verbose_name='Аудитория')
    type = models.CharField(max_length=20, verbose_name='Тип занятия')
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class LessonStudentInfo(models.Model):
    student = models.ForeignKey(Kid, verbose_name='Студент', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, verbose_name='Урок', on_delete=models.CASCADE)
    mark = models.CharField(max_length=2,choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),('УП','УП'),('Н','Н')], blank=True)
    commendation = models.TextField(verbose_name='Похвала', blank=True)
    chastisement = models.TextField(verbose_name='Замечание', blank=True)

    class Meta:
        verbose_name = 'Результат урока для студента'
        verbose_name_plural = 'Результаты уроков для студентов'
