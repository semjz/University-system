# Generated by Django 4.2.6 on 2023-11-14 15:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_alter_addandremove_status_alter_deleteterm_result_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.CharField(choices=[('general', 'General'), ('specialized', 'Specialized'), ('core', 'Core'), ('optional', 'Optional')], max_length=11),
        ),
        migrations.AlterField(
            model_name='emergencycoursedroprequest',
            name='request_result',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=8),
        ),
        migrations.AlterField(
            model_name='student',
            name='entrance_year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1402)]),
        ),
    ]
