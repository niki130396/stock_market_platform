# Generated by Django 3.0.5 on 2021-09-09 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0004_normalizedfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancesheetfield',
            name='normalized_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='crawling.NormalizedField'),
        ),
        migrations.AddField(
            model_name='cashflowfield',
            name='normalized_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='crawling.NormalizedField'),
        ),
        migrations.AddField(
            model_name='crawlingsourcedetails',
            name='normalized_fields',
            field=models.ManyToManyField(related_name='sources', to='crawling.NormalizedField'),
        ),
        migrations.AddField(
            model_name='incomestatementfield',
            name='normalized_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='crawling.NormalizedField'),
        ),
    ]
