# Generated by Django 3.0.5 on 2020-08-31 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0014_duyurudosya'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duyurudosya',
            name='file',
            field=models.FileField(blank=True, upload_to='media'),
        ),
    ]