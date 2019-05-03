# Generated by Django 2.1.3 on 2019-04-30 10:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mainSection.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSection', '0004_auto_20190427_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customerFirstName', models.CharField(blank=True, max_length=150, null=True)),
                ('customerLastName', models.CharField(blank=True, max_length=150, null=True)),
                ('companyFirstName', models.CharField(blank=True, max_length=150, null=True)),
                ('customerAddress1', models.CharField(blank=True, max_length=150, null=True)),
                ('customerAddress2', models.CharField(blank=True, max_length=150, null=True)),
                ('customerAddress3', models.CharField(blank=True, max_length=150, null=True)),
                ('customerPhone', models.CharField(blank=True, max_length=150, null=True)),
                ('customerWhatsApp', models.CharField(blank=True, max_length=150, null=True)),
                ('archived', models.BooleanField(default='False')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('userCreated', models.CharField(max_length=500)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('userModified', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='CutomerType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customerType', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'CustomerTypes',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoiceNumber', models.CharField(blank=True, default=mainSection.models.increment_invoice_number, max_length=500, null=True)),
                ('invoiceDate', models.DateField(default=django.utils.timezone.now)),
                ('archived', models.BooleanField(default='False')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('userCreated', models.CharField(max_length=500)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('userModified', models.CharField(max_length=500)),
                ('customerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainSection.Customer')),
            ],
            options={
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ProductName', models.CharField(max_length=500)),
                ('Qty', models.PositiveIntegerField(blank=True, null=True)),
                ('unitPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('LineTotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('archived', models.BooleanField(default='False')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('userCreated', models.CharField(max_length=500)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('userModified', models.CharField(max_length=500)),
                ('InvoiceId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainSection.Invoice')),
                ('ProductId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainSection.Products')),
            ],
            options={
                'verbose_name_plural': 'InvoiceDetails',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainSection.CutomerType'),
        ),
    ]
