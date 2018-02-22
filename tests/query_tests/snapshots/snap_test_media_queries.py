# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_getting_all_medias 1'] = {
    'data': {
        'medias': {
            'edges': [
                {
                    'node': {
                        'chapters': [
                            '1',
                            '2'
                        ],
                        'externalUrl': 'http://example.com',
                        'name': 'name',
                        'order': 1,
                        'series': 'series',
                        'type': 'book'
                    }
                }
            ]
        }
    }
}

snapshots['test_getting_single_media 1'] = {
    'data': {
        'media': {
            'chapters': [
                '1',
                '2'
            ],
            'externalUrl': 'http://example.com',
            'name': 'name',
            'order': 1,
            'series': 'series',
            'type': 'book'
        }
    }
}
