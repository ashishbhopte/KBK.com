# Generated by Django 5.0 on 2024-03-05 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BKB_Home', '0011_alter_signup_model_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup_model',
            name='image',
            field=models.ImageField(null=True, upload_to='media/userimage/'),
        ),
    ]