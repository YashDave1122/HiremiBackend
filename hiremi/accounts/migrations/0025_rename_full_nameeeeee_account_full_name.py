# Generated by Django 5.1.3 on 2025-03-08 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_rename_full_name_account_full_nameeeeee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='full_nameeeeee',
            new_name='full_name',
        ),
    ]
