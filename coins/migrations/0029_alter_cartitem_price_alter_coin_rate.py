# Generated by Django 4.1.13 on 2024-04-27 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0028_cartitem_price_coin_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='coin',
            name='rate',
            field=models.FloatField(),
        ),
    ]
