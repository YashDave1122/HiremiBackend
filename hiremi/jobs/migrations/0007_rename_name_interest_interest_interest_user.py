# Generated by Django 5.1.5 on 2025-03-03 06:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='interest',
            old_name='name',
            new_name='interest',
        ),
        migrations.AddField(
            model_name='interest',
            name='user',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='interest', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
