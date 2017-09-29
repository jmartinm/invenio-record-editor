# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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

"""Invenio module for editing JSON records."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, render_template, request
from flask_login import login_required

blueprint = Blueprint(
    'invenio_record_editor',
    __name__,
    url_prefix='/editor',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
@login_required
def index(path):
    """Render base view."""
    return render_template(current_app.config['RECORD_EDITOR_INDEX_TEMPLATE'])


@blueprint.route('/preview', methods=['POST'])
def preview():
    """Preview the record being edited."""
    data = request.get_json()
    template = current_app.config['RECORD_EDITOR_PREVIEW_TEMPLATE_FUNCTION'](
        data
    )
    return render_template(template, record=data)
