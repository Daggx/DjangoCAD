# Generated by Django 3.0.5 on 2020-04-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0005_auto_20200409_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]