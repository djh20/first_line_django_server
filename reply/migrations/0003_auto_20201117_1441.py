# Generated by Django 3.1.2 on 2020-11-17 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reply', '0002_auto_20201016_0809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='edting_date',
            new_name='editing_date',
        ),
    ]
