# Generated by Django 4.2.3 on 2023-08-31 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("propertease", "0008_rename_contetnt_thread_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="thread",
            name="content",
            field=models.TextField(max_length=1000),
        ),
    ]
