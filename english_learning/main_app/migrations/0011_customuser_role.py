# Generated by Django 5.1.2 on 2024-11-09 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_remove_customuser_role_course_price_in_yen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')], max_length=10, null=True),
        ),
    ]
