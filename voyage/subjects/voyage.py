from enum import Enum

from rx.subjects import Subject

from voyage.models import Voyage


class Types(Enum):
    UPDATED = 1


class VoyageSubject:
    _subject = Subject()

    def subscribe_updated(self, voyage_id):
        return (
            self._subject
            .filter(lambda d: d['type'] == Types.UPDATED and d['id'] == voyage_id)
            .map(lambda d: Voyage.query.get(d['id']))
        )

    def trigger_updated(self, voyage):
        self._subject.on_next({'type': Types.UPDATED, 'id': voyage.id})


voyage_subject = VoyageSubject()
