# Generated by Django 5.0.6 on 2024-07-14 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_alter_openinghour_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ('day', '-from_hour')},
        ),
    ]