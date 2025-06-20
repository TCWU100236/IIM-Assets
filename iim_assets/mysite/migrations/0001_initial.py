# Generated by Django 5.2 on 2025-06-14 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "userid",
                    models.CharField(
                        max_length=10, unique=True, verbose_name="使用者編號"
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=10, verbose_name="使用者名稱"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Asset",
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
                (
                    "asset_code",
                    models.CharField(max_length=20, unique=True, verbose_name="財編"),
                ),
                ("name", models.CharField(max_length=20, verbose_name="品名")),
                (
                    "accessories",
                    models.TextField(
                        blank=True, default="暫無附件", null=True, verbose_name="附件"
                    ),
                ),
                (
                    "unit_price",
                    models.PositiveIntegerField(default=0, verbose_name="單價"),
                ),
                (
                    "brand",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="廠牌"
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="型號"
                    ),
                ),
                (
                    "origin_country",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="國別"
                    ),
                ),
                (
                    "serial_number",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="序號"
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="存放處所"
                    ),
                ),
                (
                    "lifespan_years",
                    models.PositiveIntegerField(default=0, verbose_name="使用年限"),
                ),
                (
                    "funding_source",
                    models.CharField(
                        default="不知", max_length=10, verbose_name="經費來源"
                    ),
                ),
                (
                    "asset_type",
                    models.CharField(
                        choices=[("property", "財產"), ("non_consumable", "非消耗品")],
                        max_length=20,
                        verbose_name="財產類別",
                    ),
                ),
                (
                    "purchase_date",
                    models.DateField(blank=True, null=True, verbose_name="購入日期"),
                ),
                ("note", models.TextField(blank=True, null=True, verbose_name="備註")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mysite.userprofile",
                        verbose_name="使用者",
                    ),
                ),
            ],
        ),
    ]
