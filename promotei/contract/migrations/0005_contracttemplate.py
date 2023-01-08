# Generated by Django 4.0.4 on 2023-01-05 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0004_contract_is_signed_alter_contract_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_template', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]