# Generated by Django 2.1.7 on 2019-04-26 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_auto_20190426_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Module'),
        ),
    ]
