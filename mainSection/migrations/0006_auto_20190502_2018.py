# Generated by Django 2.1.3 on 2019-05-02 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainSection', '0005_auto_20190430_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='companyFirstName',
            new_name='customerEmail',
        ),
    ]