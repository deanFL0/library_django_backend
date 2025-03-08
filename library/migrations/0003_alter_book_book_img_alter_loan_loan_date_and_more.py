# Generated by Django 5.1.6 on 2025-03-07 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_alter_shelf_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="book_img",
            field=models.ImageField(upload_to="media/book_images/"),
        ),
        migrations.AlterField(
            model_name="loan",
            name="loan_date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="loan",
            name="return_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
