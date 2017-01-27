# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2017 "Capensis" [http://www.capensis.com]
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

from __future__ import unicode_literals

from canopsis.common.ws import route
from canopsis.weather.manager import Weather


def exports(ws):

    wm = Weather()

    @route(
        ws.application.get,
        name='weather/get',
        payload=[
            'filter',
            'limit',
            'sort_key', 'sort_dir'
        ]
    )
    def get_weather(
            filter={},
            limit=100,
            sort_key='entity_id', sort_dir='ASC'
    ):
        """
        Aggregate weather data in a format that can be used by the UI weather
        widget.

        Several aggregation operations are performed :

          - Select selectors from context collection
          - Limit selectors number
          - Lookup in foreign collections (alarm, linklist, pbehavior).
            Lookups are performed as described by schema configuration.
          - Project fields so as UI can read infos more easily. Projection
            if performed as described by schema configuration.
          - Sort result documents

        A field 'entities' is added to each selector, embeding all entities
        that it selects.

        :param dict filter_: Selector context filter
        :param int limit: Maximum number of considered selectors
        :param str sort_key: Field to sort data on
        :param str sort_dir: 'ASC' or 'DESC'

        :return: List of selectors
        :rtype: list of dict
        """

        return wm.get_weather(
            filter_=filter,
            limit=limit,
            sort_key=sort_key, sort_dir=sort_dir
        )
