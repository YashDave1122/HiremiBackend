# Generated by Django 5.1.5 on 2025-02-11 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_emailotp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='father_name',
            field=models.CharField(default='father', max_length=200),
            preserve_default=False,
        ),
    ]
