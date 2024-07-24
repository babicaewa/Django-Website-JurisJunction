# Generated by Django 4.2.6 on 2023-11-07 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_professional_consult_availability_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professional',
            name='consult_availability',
        ),
        migrations.AddField(
            model_name='professional',
            name='education',
            field=models.TextField(default='NULL'),
            preserve_default=False,
        ),
    ]
