# Generated by Django 4.0.6 on 2022-10-26 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SLdatabase', '0006_remove_driver_series_racingseries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racingseries',
            name='points',
            field=models.IntegerField(max_length=10),
        ),
    ]
