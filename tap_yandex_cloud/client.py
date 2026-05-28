"""Custom client handling, including YandexCloudStream base class."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, override

import grpc
from google.protobuf import timestamp_pb2
from singer_sdk.streams import Stream
from yandex.cloud.billing.usage_records.v1 import consumption_core_pb2
from yandex.cloud.billing.usage_records.v1.consumption_core_service_pb2_grpc import (
    ConsumptionCoreServiceStub,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from singer_sdk.helpers.types import Context


@dataclass(frozen=True)
class UsageDateRange:
    """Date range for Yandex Cloud billing usage requests."""

    start_date: date
    end_date: date


def parse_config_date(value: str | date | datetime) -> date:
    """Parse config date value into a date."""
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    normalized_value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized_value).date()


def yesterday_utc(today: date | None = None) -> date:
    """Return yesterday's date in UTC."""
    current_date = today or datetime.now(UTC).date()
    return current_date - timedelta(days=1)


def calculate_usage_date_range(
    config: Mapping[str, object],
    state_date: str | date | datetime | None = None,
    today: date | None = None,
) -> UsageDateRange:
    """Calculate effective usage date range using config, state, and lookback."""
    start_date = parse_config_date(config["start_date"])

    end_date_value = config.get("end_date")
    end_date = parse_config_date(end_date_value) if end_date_value else yesterday_utc(today)

    if state_date:
        lookback_days = int(config.get("lookback_days", 7))
        state_start_date = parse_config_date(state_date) - timedelta(days=lookback_days)
        start_date = max(start_date, state_start_date)

    return UsageDateRange(start_date=start_date, end_date=end_date)


def date_to_timestamp(value: date) -> timestamp_pb2.Timestamp:
    """Convert date to protobuf timestamp at UTC midnight."""
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(datetime.combine(value, time.min, UTC))
    return timestamp


def string_decimal_to_float(value: object) -> float | None:
    """Convert Yandex StringDecimal message to float."""
    raw_value = getattr(value, "value", None)

    if not isinstance(raw_value, str) or not raw_value:
        return None

    return float(Decimal(raw_value))


def aggregation_period_value(period_name: str) -> int:
    """Return Yandex Billing aggregation period enum value."""
    normalized_period_name = period_name.upper()

    try:
        return getattr(consumption_core_pb2, normalized_period_name)
    except AttributeError as error:
        msg = f"Unsupported aggregation_period: {period_name}"
        raise ValueError(msg) from error


class YandexCloudBillingClient:
    """Low-level Yandex Cloud Billing Usage API client."""

    def __init__(
        self,
        *,
        iam_token: str,
        api_endpoint: str,
    ) -> None:
        """Initialize the Billing Usage API client."""
        credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(api_endpoint, credentials)

        self._stub = ConsumptionCoreServiceStub(channel)
        self._metadata = (("authorization", f"Bearer {iam_token}"),)

    def get_billing_account_usage_report(
        self,
        *,
        billing_account_id: str,
        start_date: date,
        end_date: date,
        aggregation_period: str,
    ) -> object:
        """Fetch billing account usage report from Yandex Cloud."""
        request = consumption_core_pb2.UsageReportRequest(
            billing_account_id=billing_account_id,
            start_date=date_to_timestamp(start_date),
            end_date=date_to_timestamp(end_date),
            aggregation_period=aggregation_period_value(aggregation_period),
        )

        return self._stub.GetBillingAccountUsageReport(
            request,
            metadata=self._metadata,
        )


class YandexCloudStream(Stream):
    """Base stream class for Yandex Cloud streams."""

    @override
    def get_records(
        self,
        context: Context | None,
    ) -> Iterable[dict]:
        """Return a generator of record-type dictionary objects."""
        _ = context
        msg = "Stream must implement get_records()."
        raise NotImplementedError(msg)
