# Generated by Django 2.1.15 on 2021-09-17 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0009_portfoliodescription_input_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfoliodescription',
            name='input_file',
        ),
    ]
