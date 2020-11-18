# Generated by Django 3.1.2 on 2020-11-17 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0004_auto_20201115_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('login_log_id', models.AutoField(primary_key=True, serialize=False)),
                ('requester_ip', models.TextField(max_length=40)),
                ('login_id', models.TextField(max_length=40)),
                ('logging_date', models.DateTimeField(auto_now_add=True)),
                ('login_result', models.TextField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ResultCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.IntegerField()),
                ('code', models.IntegerField()),
                ('code_detail', models.TextField()),
            ],
            options={
                'unique_together': {('field', 'code')},
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('requester_ip', models.TextField(max_length=40)),
                ('request_method', models.TextField(max_length=10)),
                ('url', models.TextField(max_length=20)),
                ('logging_date', models.DateTimeField(auto_now_add=True)),
                ('result_code', models.IntegerField()),
                ('result_code_detail', models.TextField(max_length=100)),
                ('requester_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='member.member')),
            ],
        ),
    ]