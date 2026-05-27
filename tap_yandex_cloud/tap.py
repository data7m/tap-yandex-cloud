"""YandexCloud tap class."""

from typing import override

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_yandex_cloud import streams


class TapYandexCloud(Tap):
    """Singer tap for YandexCloud."""

    name = "tap_yandex_cloud"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Auth Token",
            description="The token to authenticate against YandexCloud",
        ),
        th.Property(
            "project_ids",
            th.ArrayType(th.StringType(nullable=False), nullable=False),
            required=True,
            title="Project IDs",
            description="Project IDs to replicate",
        ),
        th.Property(
            "start_date",
            th.DateTimeType(nullable=True),
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType(nullable=False),
            title="API URL",
            default="https://api.mysample.com",
            description="The url for the API service",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.YandexCloudStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.GroupsStream(self),
            streams.UsersStream(self),
        ]


if __name__ == "__main__":
    TapYandexCloud.cli()
