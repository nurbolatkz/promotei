# Generated by Django 4.0.4 on 2022-12-27 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.CharField(blank=True, choices=[('SENDED', 'Sended'), ('RECEIVED', 'Received'), ('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined')], max_length=10, null=True),
        ),
    ]
