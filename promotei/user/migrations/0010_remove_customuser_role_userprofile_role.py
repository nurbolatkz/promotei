# Generated by Django 4.0.4 on 2022-12-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_userprofile_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('RENTER', 'Renter'), ('RENT_RECEIVER', 'Rent Receiver')], max_length=30, null=True),
        ),
    ]
