# Generated by Django 3.0.5 on 2021-09-09 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0005_auto_20210909_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalizedfield',
            name='statement_type',
            field=models.CharField(choices=[('income_statement', 'Income Statement'), ('balance_sheet', 'Balance Sheet'), ('cash_flow', 'Cash Flow')], default='income_statement', max_length=256),
        ),
    ]