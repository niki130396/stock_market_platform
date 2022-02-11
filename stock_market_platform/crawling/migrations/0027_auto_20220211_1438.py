# Generated by Django 3.0.5 on 2022-02-11 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0026_delete_normalizedfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialstatementline',
            name='source_statement_type',
        ),
        migrations.AddField(
            model_name='financialstatementline',
            name='statement_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='crawling.StatementTypeLocalDefinition'),
        ),
        migrations.DeleteModel(
            name='StatementTypeSourceDefinition',
        ),
    ]