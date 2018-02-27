from rx.subjects import Subject


class VoyageEvents:
    _created = Subject()
    _updated = Subject()

    def updated(self, voyage):
        self._updated.on_next(voyage)

    def subscribe_updated(self, voyage_id):
        return self._updated.filter(lambda voyage: voyage.id == voyage_id).as_observable()

    def created(self, voyage):
        self._created.on_next(voyage)

    def subscribe_created(self):
        return self._created.as_observable()


voyage = VoyageEvents()
