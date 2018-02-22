from graphene import Schema

from voyage.mutations import Mutation
from voyage.queries import Query

schema = Schema(query=Query, mutation=Mutation)
