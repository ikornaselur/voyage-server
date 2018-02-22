def test_getting_all_medias(graph_client, db_media, snapshot):
    executed = graph_client.execute(
        '''
            query {
                medias {
                    edges {
                        node {
                            series
                            order
                            name
                            type
                            chapters
                            externalUrl
                        }
                    }
                }
            }
        ''')

    assert 'errors' not in executed
    snapshot.assert_match(executed)


def test_getting_single_media(graph_client, db_media, snapshot):
    executed = graph_client.execute(
        '''
            query {{
                media (id: "{}") {{
                    series
                    order
                    name
                    type
                    chapters
                    externalUrl
                }}
            }}
        '''.format(db_media.id))

    assert 'errors' not in executed
    snapshot.assert_match(executed)
