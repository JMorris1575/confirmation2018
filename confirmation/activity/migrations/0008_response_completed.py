# Generated by Django 2.0.1 on 2018-01-22 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_page_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]