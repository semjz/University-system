# Generated by Django 4.2.6 on 2023-11-12 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('student', 'Student'), ('professor', 'Professor'), ('assistant', 'Assistant'), ('it-manager', 'It-manager')], verbose_name='role'),
        ),
    ]
