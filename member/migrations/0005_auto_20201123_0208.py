# Generated by Django 3.1.3 on 2020-11-23 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20201115_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sementicrecord',
            name='date',
            field=models.DateField(),
        ),
    ]
