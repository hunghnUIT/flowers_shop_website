# Generated by Django 3.0.4 on 2020-04-20 11:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20200419_2148'),
        ('users', '0003_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fullname',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('date_ordered', models.DateTimeField(default=datetime.datetime(2020, 4, 20, 11, 45, 56, 739564, tzinfo=utc))),
                ('status', models.BooleanField(default='False')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item_ordered', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.Item')),
            ],
        ),
    ]