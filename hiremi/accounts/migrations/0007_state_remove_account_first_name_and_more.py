# Generated by Django 5.1.5 on 2025-02-09 17:58

import datetime
import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_account_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
        migrations.AddField(
            model_name='account',
            name='birth_city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='current_city',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='current_pincode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2025, 2, 9, 17, 56, 30, 756374, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='full_name',
            field=models.CharField(default='admin', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], default='male', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='is_differently_abled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='whatsapp_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('Super Admin', 'Super Admin'), ('HR', 'HR'), ('Applicant', 'Applicant')], default='Applicant', max_length=15),
        ),
        migrations.AddField(
            model_name='account',
            name='birth_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='state_born_users', to='accounts.state'),
        ),
        migrations.AddField(
            model_name='account',
            name='current_state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='state_users', to='accounts.state'),
        ),
    ]
