# Generated by Django 3.0.8 on 2020-08-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0002_produit_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='typee',
            field=models.CharField(default='tunique', max_length=200),
        ),
    ]
