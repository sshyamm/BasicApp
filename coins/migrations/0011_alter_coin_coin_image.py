# Generated by Django 5.0.4 on 2024-04-13 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0010_alter_coin_coin_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='coin_image',
            field=models.ImageField(upload_to='coin_images/'),
        ),
    ]
