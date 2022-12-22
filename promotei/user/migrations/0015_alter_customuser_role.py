# Generated by Django 4.0.4 on 2022-12-22 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('RENTER', 'Renter'), ('RENT_RECEIVER', 'Rent Receiver')], max_length=30, null=True),
        ),
    ]
