from voyage.schema.queries import VoyageQuery


def test_getting_all_voyages(db_voyage):
    voyages = VoyageQuery.resolve_voyages('root', 'info').all()
    assert voyages == [db_voyage]


def test_getting_single_voyage(db_voyage):
    voyage = VoyageQuery.resolve_voyage('root', 'info', db_voyage.id)
    assert voyage == db_voyage
