"""Tests standard tap features using the built-in SDK tests library."""

from tap_yandex_cloud.tap import TapYandexCloud

# SAMPLE_CONFIG = {
#    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
#    # TODO: Initialize minimal tap config
# }

SAMPLE_CONFIG = {
    "billing_account_id": "test-billing-account-id",
    "iam_token": "test-iam-token",
    "start_date": "2026-05-01T00:00:00Z",
    "lookback_days": 7,
    "aggregation_period": "DAY",
}

# Run standard built-in tap tests from the SDK:
# TODO: uncomment
# TestTapYandexCloud = get_tap_test_class(
#     tap_class=TapYandexCloud,
#     config=SAMPLE_CONFIG,
# )


def test_tap_can_be_created() -> None:
    """Verify that the tap can be instantiated with minimal config."""
    tap = TapYandexCloud(config=SAMPLE_CONFIG)

    assert tap.name == "tap_yandex_cloud"


def test_tap_discovers_streams() -> None:
    """Verify that streams are discoverable."""
    tap = TapYandexCloud(config=SAMPLE_CONFIG)
    streams = tap.discover_streams()

    assert streams
