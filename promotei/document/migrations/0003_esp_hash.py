# Generated by Django 4.0.4 on 2023-01-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_remove_identitynumber_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='esp',
            name='hash',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]