# Generated by Django 3.0.5 on 2021-06-13 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_statements', '0004_statementsmetadata_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statementsmetadata',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]