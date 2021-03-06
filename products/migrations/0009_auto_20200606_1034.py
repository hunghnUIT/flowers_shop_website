# Generated by Django 3.0.4 on 2020-06-06 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20200528_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=2),
        ),
        migrations.AddField(
            model_name='item',
            name='number_item_sold',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
