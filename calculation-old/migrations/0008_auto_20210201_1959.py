# Generated by Django 2.1.15 on 2021-02-01 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0007_auto_20210107_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliocomposition',
            name='quote_id',
            field=models.CharField(max_length=50),
        ),
    ]
