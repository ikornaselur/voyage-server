import inspect
from functools import partial

import graphene
from graphene import relay
from graphene.relay.connection import PageInfo
from graphql_relay.connection.arrayconnection import connection_from_list_slice


class FieldException(Exception):
    pass


def get_type(_type):
    if isinstance(_type, str):
        from voyage import types
        try:
            result = getattr(types, _type)
        except AttributeError:
            raise ImportError("voyage.types does not expose '{}' type".format(_type))
        if not inspect.isclass(result) or not issubclass(result, graphene.ObjectType):
            raise ImportError("'{}' is not a subclass of graphene.ObjectType".format(result))
        return result
    if inspect.isfunction(_type) or isinstance(_type, partial):
        return _type()
    return _type


class Field(graphene.Field):
    @property
    def type(self):
        return get_type(self._type)


class List(graphene.List):
    @property
    def of_type(self):
        return get_type(self._of_type)


#########
# Relay #
#########

class ConnectionField(relay.ConnectionField):
    def __init__(self, type, *args, **kwargs):
        # Allow setting the max first for a connection field, defaulting to 100
        self._max_first = kwargs.pop('_max_first', 100)
        super(ConnectionField, self).__init__(type, *args, **kwargs)

    @property
    def type(self):
        return get_type(self._type)

    def connection_resolver(self, resolver, connection, root, info, **args):
        args['first'] = min(args.get('first', self._max_first), self._max_first)

        # Ignore the four base args in the resolver, they're used in the slicing below
        resolver_args = {
            key: args[key] for key in args if key not in ['first', 'last', 'before', 'after']
        }
        iterable = resolver(root, info, **resolver_args)
        if iterable is None:
            iterable = []
        if type(iterable) == list:
            _len = len(iterable)
        else:
            _len = iterable.count()
        connection = connection_from_list_slice(
            iterable,
            args,
            slice_start=0,
            list_length=_len,
            list_slice_length=_len,
            connection_type=connection,
            pageinfo_type=PageInfo,
            edge_type=connection.Edge,
        )
        connection.iterable = iterable
        connection.count = _len
        return connection

    def get_resolver(self, parent_resolver):
        return partial(self.connection_resolver, parent_resolver, self.type)
