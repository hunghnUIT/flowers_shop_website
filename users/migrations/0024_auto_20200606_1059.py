# Generated by Django 3.0.4 on 2020-06-06 03:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20200606_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 3, 59, 50, 497824, tzinfo=utc)),
        ),
    ]
