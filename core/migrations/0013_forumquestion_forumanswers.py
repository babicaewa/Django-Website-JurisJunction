# Generated by Django 4.2.6 on 2024-02-17 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_professional_location_lat_professional_location_long'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum_question_title', models.CharField(max_length=300)),
                ('forum_question', models.TextField()),
                ('view_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ForumAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('forum_question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.forumquestion')),
                ('professional_answered', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.professional')),
            ],
        ),
    ]
