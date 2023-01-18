# Generated by Django 2.1.15 on 2021-01-07 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0005_auto_20210107_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencycode',
            name='currency',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='currencycode',
            name='currency_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='currencycode',
            name='country_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='currencycode',
            name='currency_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
