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

from canopsis.configuration.configurable.registry import ConfigurableRegistry
from canopsis.configuration.configurable.decorator import add_category
from canopsis.configuration.configurable.decorator import conf_paths

from canopsis.timeserie.timewindow import Period
from canopsis.timeserie.core import TimeSerie
from canopsis.task.core import get_task

from canopsis.old.mfilter import check

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins


CONF_PATH = 'serie/manager.conf'
CATEGORY = 'SERIE'
CONTENT = []


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class Serie(ConfigurableRegistry):

    CONTEXT_MANAGER = 'context'
    PERFDATA_MANAGER = 'perfdata'

    def __init__(self, context=None, perfdata=None, *args, **kwargs):
        super(Serie, self).__init__(*args, **kwargs)

        if context is not None:
            self[Serie.CONTEXT_MANAGER] = context

        if perfdata is not None:
            self[Serie.PERFDATA_MANAGER] = perfdata

    def build_mfilter_from_regex(self, regex):
        regex_parts = regex.split(' ')
        regex = {
            'component': [],
            'resource': [],
            'name': []
        }

        for part in regex_parts:
            if part.startswith('co:'):
                regex['component'].append({'$regex': part[3:]})

            elif part.startswith('re:'):
                regex['resource'].append({'$regex': part[3:]})

            elif part.startswith('me:'):
                regex['name'].append({'$regex': part[3:]})

            else:
                for key in regex.keys():
                    regex[key].append({'$regex': part})

        mfilter = {'$and': []}

        for key in regex:
            if len(regex[key]) > 0:
                local_mfilter = {'$or': [
                    subfilter for subfilter in regex[key]
                ]}

                if len(local_mfilter['$or']) == 1:
                    local_mfilter = local_mfilter['$or'][0]

                mfilter['$and'].append(local_mfilter)

        return mfilter

    def get_metrics(self, regex, metrics=None):
        mfilter = self.build_mfilter_from_regex(regex)

        if metrics is None:
            metric_ids = self[Serie.PERFDATA_MANAGER].get_metrics(mfilter)
            return self[Serie.CONTEXT_MANAGER].get_entities(metric_ids)

        else:
            result = [
                metric
                for metric in metrics
                if check(mfilter, metric)
            ]

            return result

    def get_perfdata(self, metrics, period=None, timewindow=None):
        result = {}

        for metric in metrics:
            mid = self[Serie.CONTEXT_MANAGER].get_entity_id(metric)
            perfdata = self[Serie.PERFDATA_MANAGER].get(
                mid,
                period=period,
                timewindow=timewindow
            )

            result[mid] = {
                'entity': metric,
                'points': perfdata
            }

        return result

    def aggregation(self, serieconf, timewindow=None):
        interval = serieconf.get('aggregation_interval', None)

        if interval is None:
            period = TimeSerie.VPERIOD

        else:
            period = Period(second=interval)

        ts = TimeSerie(
            period=period,
            aggregation=serieconf.get(
                'aggregation_method',
                TimeSerie.VDEFAULT_AGGREGATION
            ),
            round_time=serieconf.get(
                'round_time_interval',
                TimeSerie.VROUND_TIME
            )
        )

        metrics = self.get_metrics(serieconf['metric_filter'])
        perfdatas = self.get_perfdata(metrics, timewindow=timewindow)

        for key in perfdatas:
            perfdatas[key]['aggregated'] = ts.calculate(
                perfdatas[key]['points'],
                timewindow
            )

        return perfdatas

    def consolidation(self, serieconf, perfdatas):
        restricted_globals = {
            '__builtins__': safe_builtins,
        }

        operatorset = get_task('serie.operatorset')
        operators = operatorset(self, serieconf, perfdatas)
        restricted_globals.update(operators)

        # all perfdata are aggregated with the same period
        # so all x values are the same
        mid = perfdatas.keys()[0]
        axis_x = [point[0] for point in perfdatas[mid]['aggregated']]
        consolidated_points = []

        for x in axis_x:
            restricted_globals['x'] = x
            expression = 'result = {0}'.format(serieconf['formula'])
            code = compile_restricted(expression, '<string>', 'exec')

            exec(code) in restricted_globals

            consolidated_points.append((x, restricted_globals['result']))

        return consolidated_points

    def calculate(self, serieconf, timewindow=None):
        perfdatas = self.aggregation(serieconf, timewindow)
        return self.consolidation(serieconf, perfdatas)