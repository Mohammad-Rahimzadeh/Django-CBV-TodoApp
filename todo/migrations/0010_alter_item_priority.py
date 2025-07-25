# Generated by Django 5.2.1 on 2025-06-07 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0009_item_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="priority",
            field=models.CharField(
                blank=True,
                choices=[
                    ("High priority", "High priority"),
                    ("Medium priority", "Medium priority"),
                    ("Low priority", "Low priority"),
                ],
                max_length=15,
                null=True,
            ),
        ),
    ]
