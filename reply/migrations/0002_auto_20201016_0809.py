# Generated by Django 3.1.1 on 2020-10-16 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reply', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='edting_date',
            field=models.DateTimeField(null=True),
        ),
    ]
