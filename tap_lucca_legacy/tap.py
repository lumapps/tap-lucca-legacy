"""LuccaLegacy tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_lucca_legacy import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TapLuccaLegacy(Tap):
    """Singer tap for LuccaLegacy."""

    name = "tap-lucca-legacy"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType(nullable=False),
            required=True,
            title="API key",
            description="The API key used to call Lucca legacy API",
        ),
        th.Property(
            "api_url",
            th.StringType(nullable=False),
            required=True,
            title="API URL",
            default="https://api.mysample.com",
            description="The url for the API service",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.LuccaLegacyStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.EmployeesStream(self),
            streams.EstablishmentsStream(self),
            streams.DepartmentsStream(self),
            streams.WorkcyclesStream(self),
            streams.LegalUnitsStream(self),
            streams.WorkContractsStream(self),
            streams.RolesStream(self),
            streams.CostCentersStream(self),
            streams.LocationsStream(self),
            streams.UserlogsDepartmentStream(self),
            streams.UserlogsLegalentityStream(self),
            streams.UserlogsCostcenterStream(self),
            streams.UserlogsLocationStream(self),
        ]


if __name__ == "__main__":
    TapLuccaLegacy.cli()
