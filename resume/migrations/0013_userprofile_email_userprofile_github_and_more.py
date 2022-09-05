# Generated by Django 4.1 on 2022-09-01 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0012_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
    ]
