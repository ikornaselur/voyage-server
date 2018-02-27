from rx import Observable
from rx.subjects import Subject

import graphene

from voyage import fields

voyage_subject = Subject()


class VoyageSubscription(object):
#     voyage = fields.Field(
#         'Voyage',
#         id=fields.ID(required=True),
#     )
# 
#     def resolve_voyage(root, info, id):
#         print("Whoa damn")
#         return voyage_subject.as_observable().take_while(lambda x: True)

    count_seconds = graphene.Float(up_to=graphene.Int())

    def resolve_count_seconds(root, info, up_to=5):
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)
