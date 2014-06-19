#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------
# Copyright (c) 2014 "Capensis" [http://www.capensis.com]
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

from cconfiguration import Category, Parameter

from ctimeserie.timewindow import Period, get_offset_timewindow

from cstorage.manager import Manager

from ccontext import Context

from collections import Iterable

from time import time

DEFAULT_PERIOD = Period(**{Period.HOUR: 24})
DEFAULT_AGGREGATION = 'MEAN'

DEFAULT_DATA_TYPE = 'metric'


class PerfData(Manager):
    """
    Dedicated to access to perfdata (via periodic and timed stores).
    """

    DEFAULT_CONFIGURATION_FILE = '~/etc/perfdata.conf'

    CONTEXT = 'context'
    PERFDATA_STORAGE = 'perfdata_storage'

    def __init__(
        self, context=None, data_type=DEFAULT_DATA_TYPE,
        *args, **kwargs
    ):

        super(Manager, self).__init__(data_type=data_type, *args, **kwargs)

        self.perfdata_storage = perfdata_storage

        self.context = context

    def count(self, data_id, aggregation=None, period=None, timewindow=None):

        aggregation, period = self.get_aggregation_and_period(data_id=data_id,
            aggregation=aggregation, period=period)

        result = self.periodic_store.count(data_id=data_id, aggregation=aggregation,
            period=period, timewindow=timewindow)

        return result

    def get(self, data_id, with_meta=True, aggregation=None, period=None,
        timewindow=None, limit=0):
        """
        Get a set of data related to input data_id on the timewindow \
        and input period.
        If with_meta, result is a couple of (points, list of meta by timestamp).
        """

        aggregation, period = self.get_aggregation_and_period(data_id=data_id,
            aggregation=aggregation, period=period)

        result = self.periodic_store.get(data_id=data_id,
            aggregation=aggregation, period=period, timewindow=timewindow, limit=limit)

        if with_meta is not None:

            meta = self.timed_store.get(data_id=data_id, timewindow=timewindow)

            result = result, meta

        return result

    def get_point(self, data_id, with_meta=True, aggregation=None, period=None,
        timestamp=time()):
        """
        Get the closest point before input timestamp. Add meta informations \
        if with_meta.
        """

        aggregation, period = self.get_aggregation_and_period(data_id=data_id,
            aggregation=aggregation, period=period)

        timewindow = get_offset_timewindow(timestamp)

        result = self.periodic_store.get(data_id=data_id,
            aggregation=aggregation, period=period, timewindow=timewindow,
            limit=1)

        if with_meta is not None:

            meta = self.timed_store.get(data_id=data_id, timewindow=timewindow)

            result = result, meta

        return result

    def get_meta(self, data_id, timewindow=None, limit=0, sort=None):
        """
        Get the meta data related to input data_id and timewindow.
        """

        if timewindow is None:
            timewindow = get_offset_timewindow()
        result = self.timed_store.get(
            data_id=data_id, timewindow=timewindow, limit=limit, sort=sort)

        return result

    def put(self, data_id, points_or_point, meta=None, aggregation=None,
        period=None):
        """
        Put a (list of) couple (timestamp, value), a meta into rated_documents
        related to input period.
        kwargs will be added to all document in order to extend periodic_documents
        documents.
        """

        # if points_or_point is a point, transform it into a tuple of couple
        if len(points_or_point) > 0:
            if not isinstance(points_or_point[0], Iterable):
                points_or_point = (points_or_point,)

        aggregation, period = self.get_aggregation_and_period(data_id=data_id,
            aggregation=aggregation, period=period)

        self.periodic_store.put(data_id=data_id, aggregation=aggregation,
            period=period, points=points_or_point)

        if meta is not None:

            min_timestamp = min([point[0] for point in points_or_point])

            self.timed_store.put(data_id=data_id, value=meta, timestamp=min_timestamp)

    def remove(self, data_id, with_meta=False, aggregation=None, period=None,
        timewindow=None):
        """
        Remove values and meta of one metric.
        meta_names is a list of meta_data to remove. An empty list ensure that
        no meta data is removed.
        if meta_names is None, then all meta_names are removed.
        """

        aggregation, period = self.get_aggregation_and_period(data_id=data_id,
            aggregation=aggregation, period=period)

        self.periodic_store.remove(data_id=data_id, aggregation=aggregation,
            period=period, timewindow=timewindow)

        if with_meta:
            self.timed_store.remove(data_id=data_id, timewindow=timewindow)

    def update_meta(self, data_id, meta, timestamp=None):
        """
        Update meta information.
        """

        self.timed_store.put(data_id=data_id, value=meta, timestamp=timestamp)

    def remove_meta(self, data_id, timewindow=None):
        """
        Remove meta information.
        """

        self.timed_store.remove(data_id=data_id, timewindow=timewindow)

    def get_entity(self, data_id):
        """
        Get entity related to input data_id.

        TODO: ensure the access is provided by a referential API instead of MONGODB
        """

        result = None

        query = {
            'nodeid': data_id,
            'type': self.data_type
        }

        cursor = self.entities.find(query)
        cursor.hint([('type', 1), ('nodeid', 1)])

        try:
            result = cursor[0]
        except IndexError:
            pass

        return result

    def get_aggregation_and_period(self, data_id, aggregation=None, period=None):
        """
        Get default aggregation and period related to input data_id.
        (DEFAULT_AGGREGATION, DEFAULT_PERIOD) if related entity does not exist or
        does not contain a default aggregation or period.
        """

        result = aggregation, period

        if None in result:

            if aggregation is None:
                aggregation = DEFAULT_AGGREGATION

            if period is None:
                period = DEFAULT_PERIOD

            entity = self.get_entity(data_id=data_id)

            if entity is not None:
                if result[0] is None:
                    result = entity.get('aggregation', DEFAULT_AGGREGATION), result[1]

                if result[1] is None:
                    result = result[0], entity.get('period', DEFAULT_PERIOD)

            else:
                result = (
                    aggregation if aggregation is not None else DEFAULT_AGGREGATION,
                    period if period is not None else DEFAULT_PERIOD)

        return result

    def _conf(self, *args, **kwargs):

        result = super(PerfData, self)._conf(*args, **kwargs)

        category = self._get_category()

        result += Category(category,
            Parameter(Perfdata.CONTEXT),
            Parameter(Perfdata.PERFDATA_STORAGE))

        return result