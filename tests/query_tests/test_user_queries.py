def test_getting_current_user(graph_client, db_user, client, snapshot):
    with client.use(db_user):
        executed = graph_client.execute(
            '''
                query {
                    currentUser {
                        name
                        email
                    }
                }
            ''')

    snapshot.assert_match(executed)
