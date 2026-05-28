"""Stream type classes for tap-yandex-cloud."""

from __future__ import annotations

from typing import ClassVar

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_yandex_cloud.client import YandexCloudStream


class BillingAccountUsageDailyStream(YandexCloudStream):
    """Daily billing account usage stream."""

    name = "billing_account_usage_daily"
    primary_keys: ClassVar[list[str]] = ["billing_account_id", "usage_date"]
    replication_key = "usage_date"
    is_sorted = True

    schema = th.PropertiesList(
        th.Property(
            "billing_account_id",
            th.StringType,
            required=True,
            description="Yandex Cloud billing account ID.",
        ),
        th.Property(
            "usage_date",
            th.DateType,
            required=True,
            description="Usage date in UTC.",
        ),
        th.Property(
            "aggregation_period",
            th.StringType,
            description="Aggregation period used by Yandex Billing API.",
        ),
        th.Property(
            "currency",
            th.StringType,
            description="Billing account currency.",
        ),
        th.Property(
            "cost",
            th.NumberType,
            description="Raw usage cost before credits and discounts.",
        ),
        th.Property(
            "expense",
            th.NumberType,
            description="Final billable amount after credits and discounts.",
        ),
        th.Property(
            "extracted_at",
            th.DateTimeType,
            description="Record extraction timestamp in UTC.",
        ),
    ).to_dict()
