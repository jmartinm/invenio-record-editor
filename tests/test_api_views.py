# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""API Views tests."""

from __future__ import absolute_import, print_function

import json
import mock

from helpers import other_simple_check, simple_check


def test_validate_no_validation_fns(app):
    data = {
        '$schema': 'schema',
        'title': 'My title'
    }
    with app.test_client() as client:
        res = client.post("/editor/validate", data=data)
        assert res.status_code == 200
        assert {} == json.loads(res.data)


def test_validate_with_validation_fns(app):
    data = {
        '$schema': 'schema',
        'title': 'My title',
        'hello': 'world'
    }

    extra_config = {
        'RECORD_EDITOR_VALIDATOR_FUNCTIONS': [simple_check, other_simple_check]
    }

    with app.test_client() as client:
        with mock.patch.dict(app.config, extra_config):
            res = client.post(
                "/editor/validate",
                data=json.dumps(data),
                content_type='application/json'
            )
            assert res.status_code == 200

            expected = {
                "hello": [
                    {
                        'message': 'Hello should not be equal to world',
                        'type': 'warning'
                    },
                    {
                        'message': 'Hello and world are not compatible',
                        'type': 'error'
                    }
                ]
            }
            assert expected == json.loads(res.data)
