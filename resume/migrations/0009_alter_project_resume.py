# Generated by Django 4.1 on 2022-08-28 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0008_alter_project_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resume', to='resume.resume'),
        ),
    ]
