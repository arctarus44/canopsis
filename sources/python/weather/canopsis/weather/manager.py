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
        """
        Weather aggregation is built with the help of the schema in order to
        have somewhat configurable queries.
        """

        if not hasattr(self, '_weather_aggr'):
            self._weather_aggr = get_schema('weather_aggregation')

        return self._weather_aggr

    def context_entities_aggr(self, filter_, limit):
        """
        Part of the weather aggregation responsible to fetch context entities.

        :param dict filter_: Context filter
        :param int limit: Maximum number of entities

        :return: List of aggregations
        :rtype: list of dict
        """

        return [
            {
                '$match': filter_
            },
            {
                '$limit': limit
            }
        ]

    def alarm_lookup_aggr(self):
        """
        Part of the weather aggregation adding entity_id current alarm fields.

        :return: List of aggregations
        :rtype: list of dict
        """

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
        """
        Part of the weather aggregation adding entity_id linklist fields.

        :return: List of aggregations
        :rtype: list of dict
        """

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
        """
        Part of the weather aggregation adding entity_id pbehaviors.

        :return: List of aggregations
        :rtype: list of dict
        """

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
        """
        Proxy applying necessary lookup aggregations as described in the
        configuration.

        :return: List of aggregations
        :rtype: list of dict
        """

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
        """
        Part of the weather aggregation keeping or aliasing fields as described
        in the configuration.

        :return: List of aggregations
        :rtype: list of dict
        """

        conf = self.weather_aggr.get('ui_projection')

        projection = [{'$project': conf}]

        return projection

    def sort_aggr(self, sort_key, sort_dir):
        """
        Part of the weather aggregation sorting result documents.

        :param str sort_key: Field to be sorted
        :param str sort_dir: 'ASC' or 'DESC'

        :return: List of aggregations
        :rtype: list of dict

        :raises ValueError: If sort_dir is neither 'ASC' nor 'DESC'
        """

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
        """
        Get entities selected by a selector.

        :param str selector_id: entity_id of selector

        :return: List of entities
        :rtype: list of dict
        """

        return []

    def get_weather(
            self,
            filter_,
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

        aggr = []

        aggr += self.context_entities_aggr(filter_=filter_, limit=limit)
        aggr += self.lookups_aggr()
        aggr += self.weather_projection_aggr()
        aggr += self.sort_aggr(sort_key=sort_key, sort_dir=sort_dir)

        items = self['context_storage']._backend.aggregate(aggr)

        # It might be performable with an aggregation, saving a lot of
        # execution time
        for i in items:
            i['entities'] = self.get_entities(i['entity_id'])

        return items
