# Generated by Django 5.2.1 on 2025-07-16 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_profile_completed_task_count"),
        ("todo", "0017_remove_item_remind_me_alter_item_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to="account.profile",
            ),
        ),
    ]
