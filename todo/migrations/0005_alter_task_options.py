# Generated by Django 5.0.6 on 2024-06-25 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_alter_task_options_task_due_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['created_at', 'due_date']},
        ),
    ]