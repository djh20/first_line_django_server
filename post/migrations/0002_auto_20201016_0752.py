# Generated by Django 3.1.1 on 2020-10-16 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_sementicrecord'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='likerecord',
            name='temperature',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='LookupRecord',
            fields=[
                ('lookup_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('temperature', models.FloatField()),
                ('is_like', models.BooleanField()),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.member')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
    ]