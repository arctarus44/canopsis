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

from canopsis.configuration.configurable import Configurable
from canopsis.configuration.configurable.decorator import conf_paths
from canopsis.configuration.configurable.decorator import add_category
from canopsis.configuration.model import Parameter

from canopsis.timeserie.timewindow import Period, TimeWindow
from canopsis.common.template import Template
from canopsis.event.sla import SlaEvent
from canopsis.event.check import Check

from time import time


CONF_PATH = 'sla/manager.conf'
CATEGORY = 'SLA'
CONTENT = [
    Parameter('template'),
    Parameter('timewindow'),
    Parameter('warn', parser=float),
    Parameter('crit', parser=float)
]


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class SlaManager(Configurable):

    ALERTS_MANAGER = 'alerts_manager'
    CONTEXT_MANAGER = 'context_manager'

    def __init__(
        self,
        template=None,
        timewindow=None,
        warn=None,
        crit=None,
        alerts_manager=None,
        context_manager=None,
        *args, **kwargs
    ):
        super(SlaManager, self).__init__(*args, **kwargs)

        if template is not None:
            self.template = template

        if timewindow is not None:
            self.timewindow = timewindow

        if warn is not None:
            self.warn = warn

        if crit is not None:
            self.crit = crit

        if alerts_manager is not None:
            self[SlaManager.ALERTS_MANAGER] = alerts_manager

        if context_manager is not None:
            self[SlaManager.CONTEXT_MANAGER1] = context_manager

    def get_event(
        self,
        entity,
        template=None,
        timewindow=None,
        warn=None,
        crit=None
    ):
        if template is None:
            template = self.template

        if timewindow is None:
            timewindow = self.timewindow

        if warn is None:
            warn = self.warn

        if crit is None:
            crit = self.crit

        period = Period(second=timewindow)
        ts = time()
        timewindow = TimeWindow(
            start=period.round_timestamp(ts),
            stop=period.round_timestamp(ts, next_period=True)
        )

        alarms = self[SlaManager.ALERTS_MANAGER].get_alarm_history(
            entity,
            timewindow
        )

        # find all state steps
        steps = []

        for alarm in alarms:
            steps += [
                step
                for step in alarm['steps']
                if step['t'] in ['stateinc', 'statedec']
                and step['t'] >= timewindow.start()
            ]

        # calculate duration for each step
        totaltime = timewindow.stop() - steps[0]['t']

        durations = [
            {
                'state': steps[i]['val'],
                'duration': steps[i + 1]['t'] - steps[i]['t']
            }
            for i in range(len(steps))
        ]
        durations.append({
            'state': steps[-1]['val'],
            'duration': timewindow.stop() - steps[-1]['t']
        })

        # calculate cumulative duration for each state
        duration_per_state = {
            Check.get_state_str(state): sum([
                item['duration']
                for item in durations
                if item['state'] == state
            ])
            for state in [
                Check.OK,
                Check.MINOR,
                Check.MAJOR,
                Check.CRITICAL
            ]
        }

        # calculate percentage of each state
        percents = {
            state: 100.0 * duration_per_state[state] / totaltime
            for state in map(Check.get_state_str, [
                Check.OK,
                Check.MINOR,
                Check.MAJOR,
                Check.CRITICAL
            ])
        }

        # generate metrics
        metrics = [
            {
                'metric': 'cps_pct_by_{0}'.format(state),
                'value': percents[state],
                'max': 100
            }
            for state in percents
        ]

        metrics += [
            {
                'metric': 'cps_availability_percent',
                'value': percents[Check.OK],
                'max': 100,
                'warn': warn,
                'crit': crit
            },
            {
                'metric': 'cps_availability_duration',
                'value': duration_per_state[Check.OK],
                'unit': 's'
            },
            {
                'metric': 'cps_alerts_percent',
                'value': sum([
                    percents[Check.get_state_str(state)]
                    for state in [Check.MINOR, Check.MAJOR, Check.CRITICAL]
                ]),
                'max': 100
            },
            {
                'metric': 'cps_alerts_duration',
                'value': sum([
                    duration_per_state[Check.get_state_str(state)]
                    for state in [Check.MINOR, Check.MAJOR, Check.CRITICAL]
                ])
            }
        ]

        # generate event
        evt_entity = self[SlaManager.CONTEXT_MANAGER].get_entity_by_id(entity)
        evt_state = Check.OK

        if percents[Check.OK] < warn:
            evt_state = Check.MINOR

        if percents[Check.OK] < crit:
            evt_state = Check.MAJOR

        tmpl = Template(template)
        tmplctx = {
            'durations': duration_per_state,
            'percents': percents
        }

        return SlaEvent.create(
            source_type='resource',
            component=evt_entity['component'],
            resource='sla',
            state=evt_state,
            metrics=metrics,
            output=tmpl(tmplctx)
        )
