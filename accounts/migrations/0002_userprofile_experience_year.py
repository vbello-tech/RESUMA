# Generated by Django 4.1.5 on 2023-08-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='experience_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
