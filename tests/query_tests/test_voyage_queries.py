def test_getting_all_voyages(graph_client, db_voyage, snapshot):
    executed = graph_client.execute(
        '''
            query {
                voyages {
                    edges {
                        node {
                            name
                            media {
                                name
                            }
                            owner {
                                name
                                email
                            }
                            members {
                                name
                                email
                            }
                        }
                    }
                }
            }
        ''')

    assert 'errors' not in executed
    snapshot.assert_match(executed)


def test_getting_single_voyage(graph_client, db_voyage, snapshot):
    executed = graph_client.execute(
        '''
            query {{
                voyage (id: "{}") {{
                    name
                    media {{
                        name
                    }}
                    owner {{
                        name
                        email
                    }}
                    members {{
                        name
                        email
                    }}
                }}
            }}
        '''.format(db_voyage.id))

    assert 'errors' not in executed
    snapshot.assert_match(executed)
