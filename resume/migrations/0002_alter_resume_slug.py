# Generated by Django 4.1.5 on 2023-08-27 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='slug',
            field=models.SlugField(default='pnnezwso21by1apc58lo'),
        ),
    ]
