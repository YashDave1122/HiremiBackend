# Generated by Django 5.1.5 on 2025-02-19 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_delete_education'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='career_stage',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
