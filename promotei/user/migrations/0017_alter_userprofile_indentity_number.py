# Generated by Django 4.0.4 on 2022-12-22 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_remove_identitynumber_birth_date_and_more'),
        ('user', '0016_alter_userprofile_indentity_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='indentity_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.identitynumber'),
        ),
    ]
