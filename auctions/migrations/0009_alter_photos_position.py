# Generated by Django 5.2 on 2025-05-06 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='position',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
