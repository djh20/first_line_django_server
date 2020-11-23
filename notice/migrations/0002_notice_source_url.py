from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='source_url',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
