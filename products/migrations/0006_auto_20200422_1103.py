# Generated by Django 3.0.4 on 2020-04-22 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200419_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]