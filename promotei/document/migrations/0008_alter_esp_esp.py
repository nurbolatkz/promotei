# Generated by Django 4.0.4 on 2023-01-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0007_alter_esp_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esp',
            name='esp',
            field=models.FileField(upload_to=''),
        ),
    ]
