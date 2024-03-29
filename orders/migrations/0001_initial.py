# Generated by Django 4.0 on 2024-02-21 18:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.IntegerField(choices=[(1, '주문 시작'), (2, '결제 완료'), (3, '배송중'), (4, '배송 완료')], default=1)),
                ('shipping_address', models.CharField(blank=True, max_length=255, null=True)),
                ('detail_shipping_address', models.BinaryField()),
                ('total_price', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('category_name', models.CharField(max_length=255)),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_order_set', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_order_set', to='items.product')),
            ],
        ),
        migrations.AddIndex(
            model_name='productorder',
            index=models.Index(fields=['order_id', '-created_at'], name='order__created_at_desc_idx'),
        ),
        migrations.AddConstraint(
            model_name='productorder',
            constraint=models.UniqueConstraint(fields=('order_id', 'product_id'), name='unique_order_product_id'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user_id', '-created_at'], name='user__created_at_desc_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created_at'], name='created_at_desc_index'),
        ),
    ]
