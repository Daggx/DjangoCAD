# Generated by Django 2.2 on 2020-04-09 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0004_auto_20200408_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hopital',
            name='wilaya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sprint1.Wilaya'),
        ),
    ]