"""YandexCloud tap class."""

from typing import override

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_yandex_cloud import streams


class TapYandexCloud(Tap):
    """Singer tap for YandexCloud."""

    name = "tap_yandex_cloud"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "billing_account_id",
            th.StringType(nullable=False),
            required=True,
            title="Billing Account ID",
            description="Yandex Cloud billing account ID to fetch usage and cost data for.",
        ),
        th.Property(
            "iam_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="IAM Token",
            description="Yandex Cloud IAM token used to authenticate Billing Usage API requests.",
        ),
        th.Property(
            "start_date",
            th.DateTimeType(nullable=False),
            required=True,
            title="Start Date",
            description=(
                "Lower bound for usage data extraction. Used as the initial start date "
                "before state exists."
            ),
        ),
        th.Property(
            "end_date",
            th.DateTimeType(nullable=True),
            title="End Date",
            description=(
                "Optional upper bound for usage data extraction. If omitted, the tap uses "
                "yesterday in UTC."
            ),
        ),
        th.Property(
            "lookback_days",
            th.IntegerType(nullable=False),
            default=7,
            title="Lookback Days",
            description=(
                "Number of days to re-read before the last saved state date to handle late "
                "billing adjustments."
            ),
        ),
        th.Property(
            "aggregation_period",
            th.StringType(nullable=False),
            default="DAY",
            title="Aggregation Period",
            description="Yandex Billing aggregation period. For the first version, use DAY.",
        ),
        th.Property(
            "api_endpoint",
            th.StringType(nullable=False),
            default="billing.api.cloud.yandex.net:443",
            title="API Endpoint",
            description="Yandex Cloud Billing Usage gRPC API endpoint.",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.YandexCloudStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.BillingAccountUsageDailyStream(self),
        ]


if __name__ == "__main__":
    TapYandexCloud.cli()
