# Generated by Django 3.1.1 on 2020-10-17 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20201016_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_reply',
            field=models.IntegerField(default=0),
        ),
    ]