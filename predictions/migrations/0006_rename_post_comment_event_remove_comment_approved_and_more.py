# Generated by Django 4.2.16 on 2024-10-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0005_rename_event_name_event_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='event',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
