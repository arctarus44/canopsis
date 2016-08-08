# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
#
# This file is part of Canopsis.
#
# Canopsis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Canopsis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Canopsis.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------

import json
import jsonpatch

def add(path_transfo, path, value, new='add'):
    """Function to add field in the transformation patch"""
    add_prop = {}

    add_prop['op'] = 'add'
    add_prop['path'] = path
    add_prop['value'] = value

    with open(path_transfo, "r") as f:
        doc_transfo = json.load(f)

    dc_patch = doc_transfo['patch']
    dc_patch[new] = add_prop
    doc_transfo['patch'] = dc_patch

    with open(path_transfo, "w") as f:
        json.dump(doc_transfo, f, indent=4)


def copy(path_transfo, fr, path, new='copy'):
    """Function to copy field in the transformation patch"""

    copy_prop = {}

    copy_prop['op'] = 'copy'
    copy_prop['path'] = path
    copy_prop['fr'] = fr

    with open(path_transfo, "r") as f:
        doc_transfo = json.load(f)

    dc_patch = doc_transfo['patch']
    dc_patch[new] = copy_prop
    doc_transfo['patch'] = dc_patch

    with open(path_transfo, "w") as f:
        json.dump(doc_transfo, f, indent=4)


def remove(path_transfo, path, new='remove'):
    """Function to remove field in the transformation patch"""

    remove_prop = {}

    remove_prop['op'] = 'remove'
    remove_prop['path'] = path

    with open(path_transfo, "r") as f:
        doc_transfo = json.load(f)

    dc_patch = doc_transfo['patch']
    dc_patch[new] = remove_prop
    doc_transfo['patch'] = dc_patch

    with open(path_transfo, "w") as f:
        json.dump(doc_transfo, f, indent=4)


def replace(path_transfo, path, value, new='replace'):
    """Function to replace field by another in the transformation patch"""

    replace_prop = {}

    replace_prop['op'] = 'replace'
    replace_prop['path'] = path
    replace_prop['value'] = value

    with open(path_transfo, "r") as f:
        doc_transfo = json.load(f)

    dc_patch = doc_transfo['patch']
    dc_patch[new] = replace_prop
    doc_transfo['patch'] = dc_patch

    with open(path_transfo, "w") as f:
        json.dump(doc_transfo, f, indent=4)