# Generated by Django 2.1.3 on 2018-12-26 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSection', '0003_auto_20181220_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='productImg',
            field=models.ImageField(blank=True, max_length=5000, null=True, upload_to='D:\\MY\\My Projects\\software projects\\shadesProductUploader\\src\\shadesProductUploader\\media'),
        ),
    ]
