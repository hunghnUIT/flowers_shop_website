# Generated by Django 3.0.4 on 2020-05-28 06:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20200526_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 28, 6, 23, 10, 929804, tzinfo=utc)),
        ),
    ]
