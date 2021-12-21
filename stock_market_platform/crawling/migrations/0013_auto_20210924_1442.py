# Generated by Django 3.0.5 on 2021-09-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0012_auto_20210912_1124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='normalizedfield',
            old_name='name',
            new_name='target_name',
        ),
        migrations.AddField(
            model_name='normalizedfield',
            name='name_from_source',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]