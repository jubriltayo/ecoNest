# Generated by Django 5.0.7 on 2024-08-25 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_productimages_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='life',
            field=models.CharField(blank=True, default='100 Days', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='mfd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.CharField(blank=True, default='10', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(blank=True, default='Organic', max_length=100, null=True),
        ),
    ]
