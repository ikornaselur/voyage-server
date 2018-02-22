# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_getting_current_user 1'] = {
    'data': {
        'currentUser': {
            'email': 'normal@example.com',
            'name': 'Normal User'
        }
    }
}
