

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instructors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('open_status', models.BooleanField(default=True)),
                ('thumb', models.ImageField(blank=True, default='default.png', upload_to='')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.Instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('Course', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('module', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='courses.Module')),
            ],
        ),
        migrations.CreateModel(
            name='QuizChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('value', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.QuizQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text_content', models.TextField()),
                ('image_content', models.ImageField(blank=True, default='default.png', upload_to='')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('Module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Module')),
                ('question_text', models.CharField(max_length=200)),
                ('module', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='courses.Module')),
            ],
        ),
    ]
