# Generated by Django 3.1.2 on 2020-11-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20201115_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lookuprecord',
            name='is_like',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lookuprecord',
            name='temperature',
            field=models.FloatField(default=0.0),
        ),
    ]
