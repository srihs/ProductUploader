# Generated by Django 2.1.3 on 2019-01-20 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='dateModified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='dateModified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetail',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='shipmentdetail',
            name='dateModified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
