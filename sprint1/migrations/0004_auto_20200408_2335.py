# Generated by Django 2.2 on 2020-04-08 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0003_auto_20200408_2240'),
    ]

    operations = [
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]