# Generated by Django 3.1.1 on 2020-10-16 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20201016_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='edting_date',
            field=models.DateTimeField(null=True),
        ),
    ]
