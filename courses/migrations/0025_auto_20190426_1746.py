# Generated by Django 2.1.7 on 2019-04-26 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_remove_course_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='module',
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='course',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
    ]
