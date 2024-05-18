# Generated by Django 5.0.6 on 2024-05-18 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_product_image_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='out',
            name='returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_code/'),
        ),
        migrations.AlterField(
            model_name='return',
            name='out',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returned_set', to='main.out'),
        ),
    ]