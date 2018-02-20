import inspect
import operator
from functools import partial, reduce

import graphene
from graphene import relay
from graphene.relay.connection import PageInfo
from graphql_relay.connection.arrayconnection import connection_from_list_slice


class FieldException(Exception):
    pass


def deep_source_resolver(source, root, info, **kwargs):
    """ Try to resolve the source from the root dynamically

    Tries to handle both nested dict and nested objects, though not mixed
    together
    """
    if isinstance(root, dict):
        return reduce(lambda d, key: d.get(key, None) if isinstance(d, dict) else None, source.split('.'), root)

    try:
        resolved = operator.attrgetter(source)(root)
    except AttributeError:
        return None

    if inspect.isfunction(resolved) or inspect.ismethod(resolved):
        return resolved()
    return resolved


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


def update_source_resolver(kwargs):
    if 'source' in kwargs:
        if 'resolver' in kwargs:
            raise FieldException('Can\'t provide both source and resolver to the same field')
        source = kwargs.pop('source')
        kwargs['resolver'] = partial(deep_source_resolver, source)
    return kwargs


class Field(graphene.Field):
    def __init__(self, *args, **kwargs):
        if 'source' in kwargs:
            source = kwargs.pop('source')
            kwargs['resolver'] = partial(deep_source_resolver, source)
        super(Field, self).__init__(*args, **kwargs)

    @property
    def type(self):
        return get_type(self._type)


class ID(graphene.ID):
    def __new__(self, *args, **kwargs):
        return graphene.ID(*args, **update_source_resolver(kwargs))


class Boolean(graphene.Boolean):
    def __new__(self, *args, **kwargs):
        return graphene.Boolean(*args, **update_source_resolver(kwargs))


class Int(graphene.Int):
    def __new__(self, *args, **kwargs):
        return graphene.Int(*args, **update_source_resolver(kwargs))


class Float(graphene.Float):
    def __new__(self, *args, **kwargs):
        return graphene.Float(*args, **update_source_resolver(kwargs))


class String(graphene.String):
    def __new__(self, *args, **kwargs):
        return graphene.String(*args, **update_source_resolver(kwargs))


class List(graphene.List):
    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **update_source_resolver(kwargs))

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
