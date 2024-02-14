# Generated by Django 4.0 on 2024-02-10 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_remove_product_product_created_at_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='product',
            name='prod_created_at_idx',
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['deleted_at', '-created_at', 'selling'], name='prod_created_at_idx'),
        ),
    ]