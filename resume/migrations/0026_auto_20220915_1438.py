# Generated by Django 3.2.15 on 2022-09-15 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0025_auto_20220915_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='end_date',
            new_name='enrollment_date',
        ),
        migrations.RenameField(
            model_name='education',
            old_name='start_date',
            new_name='graduation_date',
        ),
        migrations.AlterField(
            model_name='education',
            name='field',
            field=models.CharField(blank=True, choices=[('BACHELORS OF SCIENCE', 'BACHELORS OF SCIENCE'), ('BACHELORS OF ENGINEERING', 'BACHELORS OF ENGINEERING')], max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='slug',
            field=models.SlugField(default='6em0wglw4mp6lrl7bsmb'),
        ),
    ]
