# Generated by Django 3.0.5 on 2020-08-30 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0011_remove_duyurudosya_duyuru'),
    ]

    operations = [
        migrations.AddField(
            model_name='duyurudosya',
            name='duyuru',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='general.Duyuru'),
            preserve_default=False,
        ),
    ]