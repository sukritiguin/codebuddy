# Generated by Django 4.2.6 on 2023-10-28 06:52

import base.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0007_pdfmessage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pdfmessage",
            name="pdf_file",
            field=models.FileField(
                upload_to=base.models.PdfMessage.unique_pdf_filename,
                validators=[base.models.validate_pdf_extension],
            ),
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", ckeditor.fields.RichTextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
