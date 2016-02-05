# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2015 "Capensis" [http://www.capensis.com]
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

from canopsis.common.ws import route
from canopsis.common.utils import singleton_per_scope
from canopsis.perfdata.manager import PerfData
from canopsis.timeserie.timewindow import TimeWindow, Period
from canopsis.timeserie.core import TimeSerie


def exports(ws):

    manager = singleton_per_scope(PerfData)

    @route(ws.application.post, payload=['metric_id', 'timewindow', 'tags'])
    def perfdata_count(metric_id, timewindow=None, tags=None):
        if timewindow is not None:
            timewindow = TimeWindow(**timewindow)

        result = manager.count(
            metric_id=metric_id, timewindow=timewindow, tags=tags
        )

        return result

    @route(
        ws.application.post,
        payload=[
            'metric_id', 'with_tags',
            'limit', 'skip', 'period',
            'timewindow', 'period', 'timeserie'
        ]
    )
    def perfdata(
        metric_id, timewindow=None, period=None, with_tags=True,
        limit=0, skip=0, timeserie=None, tags=None
    ):
        if timewindow is not None:
            timewindow = TimeWindow(**timewindow)

        if timeserie is not None:
            if period is None:
                period = timeserie.pop('period', None)

            timeserie = TimeSerie(**timeserie)

            if period is not None:
                timeserie.period = Period(**period)

        if not isinstance(metric_id, list):
            metrics = [metric_id]

        else:
            metrics = metric_id

        result = []

        for metric_id in metrics:
            # tags -> _meta
            pts, tags = manager.get(
                metric_id=metric_id, with_tags=True,
                timewindow=timewindow, limit=limit, skip=skip,
                tags=tags
            )

            tags['data_id'] = metric_id

            if timeserie is not None:
                pts = timeserie.calculate(pts, timewindow, tags=tags)

            if with_tags:
                result.append({
                    'points': pts,
                    'tags': [tags]
                })

            else:
                result.append({
                    'points': pts
                })

        return (result, len(result))

    @route(ws.application.put, payload=['metric_id', 'points', 'tags'])
    def perfdata(metric_id, points, tags=None):
        manager.put(metric_id=metric_id, points=points, tags=tags)

        result = points

        return result

    @route(ws.application.delete, payload=['metric_id', 'timewindow', 'tags'])
    def perfdata(metric_id, timewindow=None, tags=None):
        if timewindow is not None:
            timewindow = TimeWindow(**timewindow)

        manager.remove(metric_id=metric_id, timewindow=timewindow, tags=tags)

        result = None

        return result

    @route(ws.application.get)
    def perfdata_period(metric_id):
        result = manager.get_period(metric_id)

        return result

    @route(ws.application.get)
    def perfdata_internal(metric):
        result = manager.is_internal(metric)

        return result
