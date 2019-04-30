# Generated by Django 2.2b1 on 2019-04-07 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0003_delete_quizresult'),
        ('courses', '0009_merge_20190407_0502'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.Learner')),
            ],
        ),
    ]