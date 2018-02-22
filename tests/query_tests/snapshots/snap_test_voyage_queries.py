# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_getting_all_voyages 1'] = {
    'data': {
        'voyages': {
            'edges': [
                {
                    'node': {
                        'media': {
                            'name': 'name'
                        },
                        'members': [
                            {
                                'email': 'owner@example.com',
                                'name': 'Owner User'
                            },
                            {
                                'email': 'member@example.com',
                                'name': 'Member User'
                            }
                        ],
                        'name': 'The Voyage',
                        'owner': {
                            'email': 'owner@example.com',
                            'name': 'Owner User'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['test_getting_single_voyage 1'] = {
    'data': {
        'voyage': {
            'media': {
                'name': 'name'
            },
            'members': [
                {
                    'email': 'owner@example.com',
                    'name': 'Owner User'
                },
                {
                    'email': 'member@example.com',
                    'name': 'Member User'
                }
            ],
            'name': 'The Voyage',
            'owner': {
                'email': 'owner@example.com',
                'name': 'Owner User'
            }
        }
    }
}
