# Generated by Django 4.2.3 on 2023-08-24 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("propertease", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PropertyLocation",
        ),
        migrations.AlterModelOptions(
            name="propertycategory",
            options={"verbose_name_plural": "Property Locations"},
        ),
        migrations.AlterField(
            model_name="property",
            name="owner",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
