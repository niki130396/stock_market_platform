# Generated by Django 3.0.5 on 2021-03-09 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0004_alter_options_ordering_domain'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ('domain',), 'verbose_name': 'site', 'verbose_name_plural': 'sites'},
        ),
    ]