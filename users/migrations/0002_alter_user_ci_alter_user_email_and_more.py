# Generated by Django 4.0 on 2024-02-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ci',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='hashed_email',
            field=models.BinaryField(),
        ),
    ]
