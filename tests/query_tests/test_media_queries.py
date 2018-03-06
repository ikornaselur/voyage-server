from voyage.schema.queries import MediaQuery


def test_getting_all_medias(graph_client, db_media):
    medias = MediaQuery.resolve_medias('root', 'info').all()
    assert medias == [db_media]


def test_getting_single_media(graph_client, db_media):
    media = MediaQuery.resolve_media('root', 'info', db_media.id)
    assert media == db_media
