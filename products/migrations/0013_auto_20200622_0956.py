# Generated by Django 2.2.13 on 2020-06-22 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20200622_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='topic',
            field=models.CharField(choices=[('W', 'Wedding'), ('B', 'Birthday'), ('P', 'Party'), ('V', 'Valentine'), ('T', 'Tet')], default='W', max_length=2),
        ),
    ]