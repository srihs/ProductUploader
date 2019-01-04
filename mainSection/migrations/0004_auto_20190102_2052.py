# Generated by Django 2.1.3 on 2019-01-02 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainSection', '0003_auto_20190102_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='costType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('costType', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'CostType',
            },
        ),
        migrations.RenameField(
            model_name='shipmentcostfactor',
            old_name='itemCost',
            new_name='costItem',
        ),
        migrations.RenameField(
            model_name='shipmentcostfactor',
            old_name='itemCostPrice',
            new_name='costItemPrice',
        ),
        migrations.AddField(
            model_name='shipmentcostfactor',
            name='costItemPriceInLKR',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='shipmentcostfactor',
            name='costType',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainSection.costType'),
            preserve_default=False,
        ),
    ]