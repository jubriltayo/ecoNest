# Generated by Django 5.0.7 on 2024-11-16 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='coupon',
            field=models.ManyToManyField(blank=True, to='main.coupon'),
        ),
    ]
