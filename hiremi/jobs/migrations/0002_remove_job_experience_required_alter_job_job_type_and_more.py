# Generated by Django 5.1.4 on 2025-02-15 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='experience_required',
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('Intern', 'Intern'), ('Fresher', 'Fresher'), ('Experienced', 'Experienced')], max_length=20),
        ),
        migrations.AlterField(
            model_name='job',
            name='work_mode',
            field=models.CharField(choices=[('Remote', 'Remote'), ('Onsite', 'Onsite'), ('Hybrid', 'Hybrid')], max_length=10),
        ),
    ]
