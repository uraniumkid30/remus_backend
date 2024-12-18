# Generated by Django 5.1.3 on 2024-11-17 16:27

import applications.merchant.models.platform
import datetime
import django.core.files.storage
import django.db.models.deletion
import django.utils.timezone
import services.crypto
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=200)),
                ("company_id", models.CharField(default="111111-1111", max_length=20)),
                (
                    "phone_office",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="Telephone"
                    ),
                ),
                (
                    "phone_mobile",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Mobile Phone",
                    ),
                ),
                ("email", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PointOfSale",
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
                ("version", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "terminal_id",
                    models.CharField(
                        default=services.crypto.generate_terminal_id,
                        max_length=50,
                        unique=True,
                    ),
                ),
                (
                    "provider",
                    models.CharField(
                        choices=[("monnify", "MONNIFY"), ("paystack", "PAYSATCK")],
                        default="monnify",
                        max_length=64,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MerchantProfile",
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
                ("website", models.URLField()),
                ("name", models.CharField(max_length=256)),
                ("display_name", models.CharField(max_length=32)),
                ("tax_id", models.CharField(blank=True, max_length=32, null=True)),
                ("vat_id", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "logo",
                    models.FileField(
                        blank=True, null=True, upload_to="merchant_assets/logos/"
                    ),
                ),
                (
                    "logo_inside_qr_code",
                    models.FileField(
                        blank=True, null=True, upload_to="merchant_assets/qr_logos/"
                    ),
                ),
                (
                    "background",
                    models.FileField(
                        blank=True, null=True, upload_to="merchant_assets/backgrounds/"
                    ),
                ),
                (
                    "custom_link",
                    models.CharField(blank=True, max_length=350, null=True),
                ),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchants",
                        to="merchant.company",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchants",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MerchantPlatformSettings",
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
                    "domain",
                    models.CharField(
                        max_length=100,
                        unique=True,
                        validators=[
                            applications.merchant.models.platform._simple_domain_name_validator
                        ],
                        verbose_name="domain name",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="display name")),
                ("site_title", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "site_favicon",
                    models.FileField(
                        blank=True, null=True, upload_to="merchant_assets/favicons/"
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="platform_settings",
                        to="merchant.merchantprofile",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Merchant platform settings",
                "ordering": ["domain"],
            },
        ),
        migrations.CreateModel(
            name="QRTag",
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
                ("position", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "qr_image",
                    models.FileField(
                        editable=False,
                        null=True,
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="qrcodes",
                    ),
                ),
                (
                    "domain",
                    models.CharField(
                        blank=True, editable=False, max_length=128, null=True
                    ),
                ),
                (
                    "point_of_sale",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="qr_links",
                        to="merchant.pointofsale",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="QRScan",
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
                ("receipt_id", models.UUIDField(blank=True, editable=False, null=True)),
                (
                    "result",
                    models.CharField(
                        choices=[
                            ("init_payment", "INIT_PAYMENT"),
                            ("custom_route", "CUSTOM_ROUTE"),
                        ],
                        default="init_payment",
                        max_length=32,
                    ),
                ),
                ("user_agent", models.CharField(blank=True, max_length=256, null=True)),
                ("source", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "qr",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scan_log",
                        to="merchant.qrtag",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Store",
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
                ("address", models.CharField(blank=True, max_length=256)),
                ("opening_times", models.CharField(blank=True, max_length=256)),
                ("telephone", models.CharField(blank=True, max_length=20)),
                (
                    "merchant_store_id",
                    models.CharField(
                        blank=True,
                        help_text="Store ID used by the merchant",
                        max_length=128,
                        null=True,
                    ),
                ),
                (
                    "merchant_store_name",
                    models.CharField(
                        blank=True,
                        help_text="Store name used by the merchant",
                        max_length=128,
                        null=True,
                    ),
                ),
                (
                    "merchant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stores",
                        to="merchant.merchantprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="pointofsale",
            name="store",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="points_of_sale",
                to="merchant.store",
            ),
        ),
        migrations.CreateModel(
            name="Subscription",
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
                ("server", models.CharField(blank=True, max_length=255, null=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "app_type",
                    models.CharField(
                        choices=[("paystack", "Paystack"), ("monnify", "Monnify")],
                        default="monnify",
                        max_length=70,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("basic", "Basic"),
                            ("standard", "Standard"),
                            ("premium", "Premium"),
                        ],
                        default="basic",
                        max_length=50,
                    ),
                ),
                (
                    "category_price",
                    models.IntegerField(
                        choices=[
                            (
                                "onetime",
                                [
                                    (1000000, "BASIC #1000000"),
                                    (2000000, "STANDARD #2000000"),
                                    (3000000, "PREMIUM #3000000"),
                                ],
                            ),
                            (
                                "yearly",
                                [
                                    (120000, "BASIC #120000"),
                                    (240000, "STANDARD #240000"),
                                    (360000, "PREMIUM #360000"),
                                ],
                            ),
                            (
                                "monthly",
                                [
                                    (10000, "BASIC #10000"),
                                    (20000, "STANDARD #20000"),
                                    (30000, "PREMIUM #30000"),
                                ],
                            ),
                        ],
                        default=1000000,
                    ),
                ),
                ("price", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "billing_cycle",
                    models.SmallIntegerField(
                        choices=[
                            ("yearly", "Yearly"),
                            ("monthly", "Monthly"),
                            ("onetime", "Onetime"),
                        ],
                        default="monthly",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("live", "Live"),
                            ("demo", "Demo"),
                            ("test", "Test"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="demo",
                        max_length=100,
                        verbose_name="Status",
                    ),
                ),
                ("contract_length", models.IntegerField(blank=True, null=True)),
                (
                    "meta",
                    models.JSONField(
                        blank=True, default=dict, null=True, verbose_name="Meta"
                    ),
                ),
                (
                    "auto_renew",
                    models.BooleanField(default=False, verbose_name="Auto Renew"),
                ),
                ("fixed_contract", models.BooleanField(default=False, null=True)),
                (
                    "created",
                    models.DateField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                ("date_cancelled", models.DateField(blank=True, null=True)),
                (
                    "contract_start_date",
                    models.DateField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                ("contract_end_date", models.DateField(blank=True, null=True)),
                (
                    "billing_cycle_updated",
                    models.DateTimeField(default=datetime.datetime.now),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
            },
        ),
    ]
