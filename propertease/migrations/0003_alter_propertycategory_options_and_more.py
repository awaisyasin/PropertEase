# Generated by Django 4.2.3 on 2023-08-24 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("propertease", "0002_delete_propertylocation_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="propertycategory",
            options={"verbose_name_plural": "Property Categories"},
        ),
        migrations.AddField(
            model_name="property",
            name="property_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="propertease.propertycategory",
            ),
        ),
    ]
