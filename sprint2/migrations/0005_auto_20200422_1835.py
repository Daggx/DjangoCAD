# Generated by Django 2.2 on 2020-04-22 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sprint2', '0004_auto_20200422_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irm',
            name='id_patient',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='sprint2.Patient'),
            preserve_default=False,
        ),
    ]