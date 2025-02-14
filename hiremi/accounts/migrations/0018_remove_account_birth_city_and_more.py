# Generated by Django 5.1.5 on 2025-02-13 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_city_options_alter_city_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='birth_city',
        ),
        migrations.RemoveField(
            model_name='account',
            name='current_city',
        ),
        migrations.AddField(
            model_name='city',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
