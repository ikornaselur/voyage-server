from graphene import Schema

from voyage.schema.mutations import Mutation
from voyage.schema.queries import Query
from voyage.schema.subscriptions import Subscription

schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)
