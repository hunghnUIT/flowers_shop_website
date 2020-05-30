# Generated by Django 3.0.4 on 2020-04-22 02:47

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200419_2148'),
        ('users', '0006_auto_20200421_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='item_ordered',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_info',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AddField(
            model_name='order',
            name='items_ordered',
            field=models.ManyToManyField(to='products.Item'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 22, 2, 47, 20, 852046, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(default="", max_length=12),
        ),
    ]