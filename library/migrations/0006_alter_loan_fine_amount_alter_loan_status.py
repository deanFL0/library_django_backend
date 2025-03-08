# Generated by Django 5.1.6 on 2025-03-08 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0005_remove_finepayment_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="fine_amount",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="loan",
            name="status",
            field=models.CharField(
                choices=[("borrowed", "Borrowed"), ("returned", "Returned")],
                default="borrowed",
                max_length=10,
            ),
        ),
    ]
