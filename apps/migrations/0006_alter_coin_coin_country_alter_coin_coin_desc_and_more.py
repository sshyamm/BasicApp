# Generated by Django 5.0.4 on 2024-04-13 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_alter_coin_coin_country_alter_coin_coin_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='coin_country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='coin_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='coin_image',
            field=models.ImageField(null=True, upload_to='coin_images/'),
        ),
        migrations.AlterField(
            model_name='coin',
            name='coin_material',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='coin_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='coin_status',
            field=models.CharField(blank=True, choices=[('select', 'Select'), ('available', 'Available'), ('sold', 'Sold'), ('pending', 'Pending')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='coin_weight',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='coin_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='starting_bid',
            field=models.FloatField(null=True),
        ),
    ]