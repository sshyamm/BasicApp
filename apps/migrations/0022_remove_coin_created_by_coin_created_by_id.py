# Generated by Django 4.1.13 on 2024-04-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0021_remove_coin_created_by_id_coin_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coin',
            name='created_by',
        ),
        migrations.AddField(
            model_name='coin',
            name='created_by_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
