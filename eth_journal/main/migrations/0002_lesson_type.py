# Generated by Django 5.0.4 on 2024-04-28 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='type',
            field=models.CharField(default='Лекция', max_length=20, verbose_name='Тип занятия'),
            preserve_default=False,
        ),
    ]
