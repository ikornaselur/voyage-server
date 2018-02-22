def test_inviting_user_to_voyage(graph_client, db_voyage, db_user_owner, db_user, client):
    assert db_user not in db_voyage.members

    with client.use(db_user_owner):
        executed = graph_client.execute(
            '''
                mutation {{
                    inviteUserToVoyage (voyageId: "{}", email: "{}") {{
                        voyage {{
                            id
                        }}
                    }}
                }}
            '''.format(db_voyage.id, db_user.email)
        )

    assert 'errors' not in executed
    assert db_user in db_voyage.members


def test_inviting_user_only_allows_owner_to_do_it(graph_client, db_voyage, db_user_member, db_user, client):
    assert db_user not in db_voyage.members

    with client.use(db_user_member):
        executed = graph_client.execute(
            '''
                mutation {{
                    inviteUserToVoyage (voyageId: "{}", email: "{}") {{
                        voyage {{
                            id
                        }}
                    }}
                }}
            '''.format(db_voyage.id, db_user.email)
        )

    assert 'errors' in executed
    assert any(error['message'] == 'Only voyage owners can invite users' for error in executed['errors'])
    assert db_user not in db_voyage.members


def test_removing_a_user_from_voyage(graph_client, db_voyage, db_user_owner, db_user_member, client):
    assert db_user_member in db_voyage.members

    with client.use(db_user_owner):
        executed = graph_client.execute(
            '''
                mutation {{
                    removeUserFromVoyage (voyageId: "{}", email: "{}") {{
                        voyage {{
                            id
                        }}
                    }}
                }}
            '''.format(db_voyage.id, db_user_member.email)
        )

    assert 'errors' not in executed
    assert db_user_member not in db_voyage.members
