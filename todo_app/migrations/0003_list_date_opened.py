# Generated by Django 4.2.1 on 2023-05-09 13:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_alter_task_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='date_opened',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
