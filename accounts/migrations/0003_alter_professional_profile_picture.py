# Generated by Django 4.2.6 on 2024-04-12 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_professional_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/main/default-pfp.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
