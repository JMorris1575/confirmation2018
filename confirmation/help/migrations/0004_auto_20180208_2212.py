# Generated by Django 2.0.1 on 2018-02-09 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0003_auto_20180208_1937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helppage',
            options={'ordering': ['category', 'number']},
        ),
    ]
