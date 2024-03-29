# Generated by Django 4.0.4 on 2023-01-10 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0006_rename_is_signed_contract_is_signed_by_receiver_and_more'),
        ('message', '0007_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='contract',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='message_contract', to='contract.contract'),
        ),
    ]
