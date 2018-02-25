# Generated by Django 2.0.1 on 2018-02-25 01:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('consultants', '0002_auto_20180223_2119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='critique',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='critique',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
