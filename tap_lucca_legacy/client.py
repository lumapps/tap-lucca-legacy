"""REST client handling, including LuccaLegacyStream base class."""

from __future__ import annotations

import decimal
import sys
from typing import TYPE_CHECKING, Any, ClassVar

from singer_sdk import SchemaDirectory, StreamSchema
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseOffsetPaginator, BasePageNumberPaginator, SinglePagePaginator
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator


import logging
from tap_lucca_legacy import schemas

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Iterable

    import requests
    from singer_sdk.helpers.types import Context


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = SchemaDirectory(schemas)

class LuccaLegacyOffsetPaginator(BaseOffsetPaginator):

    def __init__(
        self,
        start_value: int,
        page_size: int,
        count_jsonpath: string,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None:
        BaseOffsetPaginator.__init__(self, start_value, page_size)
        self._count_jsonpath = count_jsonpath

    def has_more(self, response):
        count = next(extract_jsonpath(
            self._count_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        ))
        return count > (self._page_count * self._page_size)

class LuccaLegacyPageNumberPaginator(BasePageNumberPaginator):

    def __init__(self, start_value: TPageToken, page_size: int, count_jsonpath: string) -> None:
        BasePageNumberPaginator.__init__(self, start_value)
        self._count_jsonpath = count_jsonpath
        self._page_size = page_size

    def has_more(self, response):
        count = next(extract_jsonpath(
            self._count_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        ))
        return count > (self._page_count * self._page_size)

class LuccaLegacyStream(RESTStream):
    """LuccaLegacy stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$data[*]"

    stream_params :dict = {}

    default_page_size = 100

    # Update this value if necessary or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    # Json path to the total count of items for the paginator to work
    paginator = "offset"
    paginator_count_jsonpath = "data.count"

    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)

    @override
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return self.config["api_url"]

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        api_key: str = self.config["api_key"]
        return APIKeyAuthenticator(
            key="Authorization",
            value=f"lucca application={api_key}",
            location="header",
        )

    @property
    @override
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return {}

    @override
    def get_new_paginator(self) -> BaseAPIPaginator | None:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance, or ``None`` to indicate pagination
            is not supported.
        """
        match self.paginator:
            case "offset":
                return LuccaLegacyOffsetPaginator(start_value=0, 
                                                page_size=self.default_page_size, 
                                                count_jsonpath=self.paginator_count_jsonpath)
            
            case "page":
                return LuccaLegacyPageNumberPaginator(start_value=1, 
                                                page_size=self.default_page_size, 
                                                count_jsonpath=self.paginator_count_jsonpath)
            
        return SinglePagePaginator()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = self.stream_params


        match self.paginator:
            case "offset":
                params["paging"] = f"0,{self.default_page_size}"
                if next_page_token:
                    params["paging"] = f"{next_page_token},{self.default_page_size}"                

            case "page":
                params["limit"] = self.default_page_size
                params["page"] = 1
                if next_page_token:
                    params["page"] = next_page_token

        if self.replication_key:
            params["orderBy"] = f"{self.replication_key},desc"

        return params

    @override
    def prepare_request_payload(
        self,
        context: Context | None,
        next_page_token: Any | None,
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    @override
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )

    @override
    def post_process(
        self,
        row: dict,
        context: Context | None = None,
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Note: As of SDK v0.47.0, this method is automatically executed for all stream types.
        You should not need to call this method directly in custom `get_records` implementations.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row
