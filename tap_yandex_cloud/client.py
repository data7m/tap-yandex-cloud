"""Custom client handling, including YandexCloudStream base class."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, override

from singer_sdk.streams import Stream

if TYPE_CHECKING:
    from collections.abc import Iterable

    from singer_sdk.helpers.types import Context


class YandexCloudStream(Stream):
    """Stream class for YandexCloud streams."""

    @override
    def get_records(
        self,
        context: Context | None,
    ) -> Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.

        Args:
            context: Stream partition or context dictionary.

        Raises:
            NotImplementedError: If the implementation is TODO
        """
        # TODO: Write logic to extract data from the upstream source.
        # records = mysource.getall()
        # for record in records:
        #     yield record.to_dict()
        errmsg = "The method is not yet implemented (TODO)"
        raise NotImplementedError(errmsg)
