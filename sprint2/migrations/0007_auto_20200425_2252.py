# Generated by Django 2.2 on 2020-04-25 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sprint2', '0006_auto_20200423_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irm',
            name='id_patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sprint2.Patient'),
        ),
    ]
