# Generated by Django 4.2.1 on 2023-06-21 09:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hotel", "0004_alter_reservation_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="image_url",
        ),
        migrations.AddField(
            model_name="category",
            name="image_file",
            field=models.FileField(null=True, upload_to=""),
        ),
    ]