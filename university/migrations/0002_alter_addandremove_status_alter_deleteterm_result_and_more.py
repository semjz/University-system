# Generated by Django 4.2.6 on 2023-11-12 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addandremove',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=8),
        ),
        migrations.AlterField(
            model_name='deleteterm',
            name='result',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=8),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='course_condition',
            field=models.CharField(choices=[('failed', 'Failed'), ('passed', 'Passed')], max_length=6),
        ),
        migrations.AlterField(
            model_name='major',
            name='stage',
            field=models.CharField(choices=[('associate', 'Associate'), ('bachelor', 'Bachelor'), ('master', 'Master'), ('phd', 'PHD')], max_length=9),
        ),
        migrations.AlterField(
            model_name='professor',
            name='rank',
            field=models.CharField(blank=True, choices=[('instructor', 'Instructor'), ('assistant_professor', 'Assistant Professor'), ('associate_professor', 'Associate Professor'), ('full_professor', 'Full Professor')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='selectunit',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=8),
        ),
        migrations.AlterField(
            model_name='student',
            name='entrance_term',
            field=models.CharField(choices=[('Mehr', 'Mehr'), ('Bahman', 'Bahman')], max_length=6),
        ),
        migrations.AlterField(
            model_name='student',
            name='military_status',
            field=models.CharField(choices=[('permanent_exemption', 'Permanent Exemption'), ('education_exemption', 'Education Exemption'), ('end_of_service', 'End of Service'), ('included', 'Included')], max_length=20),
        ),
    ]