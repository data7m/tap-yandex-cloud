"""Stream type classes for tap-yandex-cloud."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar, cast, override

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_yandex_cloud.client import (
    YandexCloudBillingClient,
    YandexCloudStream,
    calculate_usage_date_range,
    currency_value_to_name,
    string_decimal_to_float,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from singer_sdk.helpers.types import Context


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

    @override
    def get_records(self, context: Context | None) -> Iterable[dict]:
        """Return daily billing account usage records."""
        date_range = calculate_usage_date_range(
            config=self.config,
            state_date=self.get_starting_replication_key_value(context),
        )

        billing_client = YandexCloudBillingClient(
            iam_token=cast("str | None", self.config.get("iam_token")),
            service_account_key_json=cast(
                "str | None",
                self.config.get("service_account_key_json"),
            ),
            api_endpoint=cast("str", self.config["api_endpoint"]),
        )

        response = billing_client.get_billing_account_usage_report(
            billing_account_id=self.config["billing_account_id"],
            start_date=date_range.start_date,
            end_date=date_range.end_date,
            aggregation_period=self.config["aggregation_period"],
        )

        extracted_at = datetime.now(UTC).isoformat()

        for entity in response.entities_data:
            for item in entity.periodic:
                yield {
                    "billing_account_id": self.config["billing_account_id"],
                    "usage_date": item.timestamp.ToDatetime().date().isoformat(),
                    "aggregation_period": self.config["aggregation_period"],
                    "currency": currency_value_to_name(response.currency),
                    "cost": string_decimal_to_float(item.cost),
                    "expense": string_decimal_to_float(item.expense),
                    "extracted_at": extracted_at,
                }
