# Generated by Django 3.0.7 on 2020-06-10 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_quiz_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='questions_count',
            field=models.IntegerField(default=0),
        ),
    ]
