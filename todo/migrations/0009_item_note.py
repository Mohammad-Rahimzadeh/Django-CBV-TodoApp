# Generated by Django 5.2.1 on 2025-06-05 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0008_remove_item_deadline_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="note",
            field=models.TextField(blank=True, null=True),
        ),
    ]
