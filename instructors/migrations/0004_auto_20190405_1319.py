# Generated by Django 2.1.7 on 2019-04-05 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0003_instructor_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='user',
        ),
        migrations.AddField(
            model_name='instructor',
            name='password',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
