# Generated by Django 5.0.4 on 2024-04-12 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('coin_id', models.AutoField(primary_key=True, serialize=False)),
                ('coin_image', models.URLField()),
                ('coin_name', models.CharField(max_length=100)),
                ('coin_desc', models.TextField()),
                ('coin_year', models.IntegerField()),
                ('coin_country', models.CharField(max_length=50)),
                ('coin_material', models.CharField(max_length=50)),
                ('coin_weight', models.FloatField()),
                ('starting_bid', models.FloatField()),
                ('coin_status', models.CharField(max_length=50)),
            ],
        ),
    ]
