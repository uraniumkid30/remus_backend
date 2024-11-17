# Generated by Django 5.1.3 on 2024-11-17 15:35

import applications.accounts.media
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blacklist",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("customer", "CUSTOMER"),
                    ("admin", "ADMIN"),
                    ("merchant", "MERCHANT"),
                ],
                default="customer",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="profile_picture",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=applications.accounts.media.profile_picture_upload_destination,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="verification_comment",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="verification_status",
            field=models.CharField(
                choices=[
                    ("unverified", "UNVERIFIED"),
                    ("pending", "PENDING"),
                    ("failed", "FAILED"),
                    ("verified", "VERIFIED"),
                ],
                default="unverified",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="blacklist",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.CreateModel(
            name="Documents",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "document_type",
                    models.CharField(
                        choices=[
                            (
                                "id",
                                [
                                    ("nin", "NIN"),
                                    ("drivers_licence", "DRIVERS_LICENSE"),
                                ],
                            ),
                            (
                                "utility_bill",
                                [
                                    ("electricity_bill", "ELECTRICITY_BILL"),
                                    ("waste_bill", "WASTE_BILL"),
                                ],
                            ),
                        ],
                        default="nin",
                        max_length=100,
                    ),
                ),
                (
                    "document_category",
                    models.CharField(
                        choices=[("id", "ID"), ("utility_bill", "UTILITY_BILL")],
                        default="id",
                        max_length=100,
                    ),
                ),
                (
                    "docunment_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "upload",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=applications.accounts.media.document_upload_destination,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
    ]
