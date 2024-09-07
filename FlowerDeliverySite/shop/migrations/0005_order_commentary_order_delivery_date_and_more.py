# Generated by Django 5.0.6 on 2024-09-07 18:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_customuser_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='commentary',
            field=models.TextField(default='Комментарий'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_place',
            field=models.TextField(default='Место доставки'),
        ),
    ]
