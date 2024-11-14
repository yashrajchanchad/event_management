# Generated by Django 5.1.1 on 2024-11-13 14:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='created_at',
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]