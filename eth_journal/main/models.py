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
    father_name = models.TextField(verbose_name='Отчество', blank=True, null=True)

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
    father_name = models.TextField(verbose_name='Отчество', blank=True, null=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
