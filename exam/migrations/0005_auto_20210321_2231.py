# Generated by Django 2.2.4 on 2021-03-21 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20210310_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='okulsınav',
            name='sınıf',
            field=models.CharField(max_length=20),
        ),
    ]
