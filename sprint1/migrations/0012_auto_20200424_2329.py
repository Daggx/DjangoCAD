# Generated by Django 2.2 on 2020-04-24 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprint1', '0011_auto_20200417_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email has already been registered.'}, max_length=254, unique=True),
        ),
    ]
