# Generated by Django 3.0.4 on 2020-05-28 14:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0017_auto_20200528_1820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_info',
        ),
        migrations.AddField(
            model_name='order',
            name='receiver',
            field=models.CharField(default='Unknown', max_length=30),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 28, 14, 42, 29, 779653, tzinfo=utc)),
        ),
    ]
