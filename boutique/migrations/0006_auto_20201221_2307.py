# Generated by Django 3.0.8 on 2020-12-21 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0005_auto_20201215_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='prix',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
