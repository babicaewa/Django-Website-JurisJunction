# Generated by Django 4.2.6 on 2023-11-07 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_professional_consult_availability_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='professional',
            old_name='education',
            new_name='school_studied',
        ),
    ]
