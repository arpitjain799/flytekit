from __future__ import absolute_import

## Todo - change this to qubole_presto once Luis's PR get's merged
from flyteidl.plugins import qubole_presto as _qubole

from flytekit.models import common as _common


class PrestoQuery(_common.FlyteIdlEntity):
    def __init__(self, routing_group, catalog, schema, statement):
        """
        Initializes a new PrestoQuery.

        :param string routing_group:
        :param string catalog:
        :param string schema:
        :param string statement:

        """
        self._routing_group = routing_group
        self._catalog = catalog
        self._schema = schema
        self._statement = statement

    @property
    def routing_group(self):
        """
        The query string.
        :rtype: str
        """
        return self._routing_group

    @property
    def catalog(self):
        """
        :rtype: int
        """
        return self._catalog

    @property
    def schema(self):
        """
        :rtype: int
        """
        return self._schema

    @property
    def statement(self):
        """
        :rtype: int
        """
        return self._statement

    def to_flyte_idl(self):
        """
        :rtype: _qubole.PrestoQuery (This needs to be updated once Luis PR is merged)
        """
        return _qubole.PrestoQuery(
            routing_group=self._routing_group,
            catalog=self._catalog,
            schema=self._schema,
            statement=self._statement
        )

    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param _qubole.PrestoQuery pb2_object:
        :return: PrestoQuery
        """
        return cls(
            query=pb2_object.routing_group,
            timeout_sec=pb2_object.catalog,
            retry_count=pb2_object.schema,
            statement=pb2_object.statement
        )
