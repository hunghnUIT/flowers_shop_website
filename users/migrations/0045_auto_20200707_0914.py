# Generated by Django 2.2.13 on 2020-07-07 02:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0044_auto_20200628_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 7, 2, 14, 2, 609491, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('1', 'Waiting Confirmation'), ('2', 'Processing'), ('3', 'Shipping'), ('4', 'Completed'), ('5', 'Requesting Cancel'), ('6', 'Canceled')], default='1', max_length=2),
        ),
    ]