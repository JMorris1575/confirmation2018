# Generated by Django 2.0.1 on 2018-01-25 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0008_response_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='timed',
            field=models.BooleanField(default=False),
        ),
    ]