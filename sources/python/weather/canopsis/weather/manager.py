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

from canopsis.middleware.registry import MiddlewareRegistry

from canopsis.tools.schema import get as get_schema

from canopsis.configuration.configurable.decorator import conf_paths
from canopsis.configuration.configurable.decorator import add_category

CONF_PATH = 'weather/manager.conf'


@conf_paths(CONF_PATH)
@add_category('WEATHER', content=[])
class Weather(MiddlewareRegistry):
    @property
    def weather_aggr(self):
        if not hasattr(self, '_weather_aggr'):
            self._weather_aggr = get_schema('weather_aggregation')

        return self._weather_aggr

    def context_entities_aggr(self, filter_, limit):
        return [
            {
                '$match': filter_
            },
            {
                '$limit': limit
            }
        ]

    def alarm_lookup_aggr(self):
        return [
            {
                '$lookup': {
                    'from': 'periodical_alarm',
                    'localField': 'entity_id',
                    'foreignField': 'd',
                    'as': 'alarm'
                }
            },
            {
                '$unwind': {
                    'path': '$alarm',
                    'preserveNullAndEmptyArrays': True
                }
            }
        ]

    def linklist_lookup_aggr(self):
        return [
            {
                '$lookup': {
                    'from': 'default_entitylink',
                    'localField': 'entity_id',
                    'foreignField': '_id',
                    'as': 'linklist'
                }
            },
            {
                '$unwind': {
                    'path': '$linklist',
                    'preserveNullAndEmptyArrays': True
                }
            }
        ]

    def pbehaviors_lookup_aggr(self):
        return [
            {
                '$lookup': {
                    'from': 'default_pbehavior',
                    'localField': 'entity_id',
                    'foreignField': 'eids',
                    'as': 'pbehaviors'
                }
            }
        ]

    def lookups_aggr(self):
        conf = self.weather_aggr.get('lookups', [])

        aggr_lookups = []
        for lookup in conf:
            if lookup == 'alarm':
                aggr_lookups += self.alarm_lookup_aggr()

            elif lookup == 'linklist':
                aggr_lookups += self.linklist_lookup_aggr()

            elif lookup == 'pbehaviors':
                aggr_lookups += self.pbehaviors_lookup_aggr()

            else:
                self.logger.warning('Unknown lookup : "{}"'.format(lookup))

        return aggr_lookups

    def weather_projection_aggr(self):
        conf = self.weather_aggr.get('ui_projection')

        projection = [{'$project': conf}]

        return projection

    def sort_aggr(self, sort_key, sort_dir):
        if sort_dir == 'ASC':
            mongo_dir = 1

        elif sort_dir == 'DESC':
            mongo_dir = -1

        else:
            raise ValueError(
                'Sort direction must be "ASC" or "DESC" (got "{}")'.format(
                    sort_dir
                )
            )

        return [{'$sort': {sort_key: mongo_dir}}]

    def get_entities(self, selector_id):
        return []

    def get_weather(
            self,
            filter_,
            limit=100,
            sort_key='entity_id', sort_dir='ASC'
    ):
        """
        """

        aggr = []

        aggr += self.context_entities_aggr(filter_=filter_, limit=limit)
        aggr += self.lookups_aggr()
        aggr += self.weather_projection_aggr()
        aggr += self.sort_aggr(sort_key=sort_key, sort_dir=sort_dir)

        items = self['context_storage']._backend.aggregate(aggr)

        for i in items:
            i['entities'] = self.get_entities(i['entity_id'])

        return items
