# Generated by Django 3.1.1 on 2020-10-16 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='suggest_amount',
            field=models.IntegerField(default=1),
        ),
    ]