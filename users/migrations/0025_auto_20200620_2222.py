# Generated by Django 3.0.4 on 2020-06-20 15:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20200606_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 20, 15, 22, 11, 134849, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('P', 'Processing'), ('S', 'Shipping'), ('C', 'Completed'), ('RC', 'Requesting Cancel')], default='P', max_length=2),
        ),
    ]
