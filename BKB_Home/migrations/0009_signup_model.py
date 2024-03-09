# Generated by Django 5.0 on 2024-03-03 08:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BKB_Home', '0008_alter_kbkform_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='signup_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_tocken', models.CharField(default=None, max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='static/userimage/')),
                ('feedback', models.TextField(blank=True, max_length=500, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]