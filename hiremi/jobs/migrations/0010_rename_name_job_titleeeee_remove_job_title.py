# Generated by Django 5.1.5 on 2025-03-04 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_job_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='name',
            new_name='titleeeee',
        ),
        migrations.RemoveField(
            model_name='job',
            name='title',
        ),
    ]
