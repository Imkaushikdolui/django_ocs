# Generated by Django 4.2.1 on 2023-06-14 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student')], max_length=60, verbose_name='role'),
        ),
    ]
