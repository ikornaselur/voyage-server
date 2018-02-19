from graphene import ObjectType, String


class TestQuery(object):
    foo = String()

    def resolve_foo(root, info):
        return "Hello, world!"


class Query(
    ObjectType,
    TestQuery,
):
    """ Combine all queries into one """
