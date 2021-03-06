# Generated by Django 3.1.1 on 2020-10-16 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('keyword', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('recent_used_date', models.DateTimeField(null=True)),
                ('suggest_amount', models.IntegerField(default=0)),
            ],
        ),
    ]
