# Generated by Django 5.0 on 2024-03-01 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BKB_Home', '0018_alter_signup_model_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup_model',
            name='feedback',
        ),
    ]
