# Generated by Django 4.1 on 2022-09-01 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0016_userprofile_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='company_description',
            field=models.CharField(default='good company', max_length=250),
        ),
    ]
