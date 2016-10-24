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
from canopsis.common.utils import route
from canopsis.sysreq.middleware import SysReq


def exports(ws):

    sysreq = SysReq()

    @route(
        ws.application.put,
        name='sysreq',
        payload=['cruds', 'ctx'],
    )
    def process(cruds, ctx=None):

        result = sysreq(cruds=cruds, ctx=ctx)

        return result

    @route(
        ws.application.post, name='sysreq/create', payload=['create', 'ctx']
    )
    def create(create, ctx=None):

        result = sysreq.driver.create(create, ctx=ctx)

        return result

    @route(ws.application.put, name='sysreq/update', payload=['update', 'ctx'])
    def update(update, ctx=None):

        result = sysreq.driver.update(update, ctx=ctx)

        return result

    @route(
        ws.application.delete, name='sysreq/delete', payload=['delete', 'ctx']
    )
    def delete(delete, ctx=None):

        result = sysreq.driver.delete(delete, ctx=ctx)

        return result

    @route(ws.application.get, name='sysreq/read', payload=['read', 'ctx'])
    def read(read, ctx=None):

        result = sysreq.driver.read(read, ctx=ctx)

        return result
