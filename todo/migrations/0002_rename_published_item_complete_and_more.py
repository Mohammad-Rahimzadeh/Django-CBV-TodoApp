# Generated by Django 5.2.1 on 2025-05-27 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="published",
            new_name="complete",
        ),
        migrations.RemoveField(
            model_name="item",
            name="description",
        ),
    ]
