# Generated by Django 5.0 on 2024-01-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BKB_Home', '0006_alter_kbkform_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbkform',
            name='Url',
            field=models.CharField(max_length=255),
        ),
    ]
