# Generated by Django 4.2.6 on 2024-03-01 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('forum', '0004_alter_forumanswers_professional_answered_and_more'),
        ('core', '0023_professional_num_of_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professional',
            name='languages',
        ),
        migrations.RemoveField(
            model_name='professional',
            name='specialties',
        ),
        migrations.RemoveField(
            model_name='professional',
            name='user',
        ),
        migrations.RemoveField(
            model_name='specialtiesaccountant',
            name='professional',
        ),
        migrations.RemoveField(
            model_name='specialtiesaccountant',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='specialtieslawyer',
            name='professional',
        ),
        migrations.RemoveField(
            model_name='specialtieslawyer',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewed_professional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.professional'),
        ),
        migrations.DeleteModel(
            name='Languages',
        ),
        migrations.DeleteModel(
            name='Professional',
        ),
        migrations.DeleteModel(
            name='Specialties',
        ),
        migrations.DeleteModel(
            name='SpecialtiesAccountant',
        ),
        migrations.DeleteModel(
            name='SpecialtiesLawyer',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
