# Generated by Django 5.1.5 on 2025-02-12 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_education'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='passing_year',
            field=models.IntegerField(),
        ),
    ]
