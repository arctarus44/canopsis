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

from canopsis.middleware.registry import MiddlewareRegistry
from canopsis.configuration.configurable.decorator import conf_paths
from canopsis.configuration.configurable.decorator import add_category
from canopsis.configuration.model import Parameter
from canopsis.context.manager import Context

from canopsis.timeserie.timewindow import (
    get_offset_timewindow, Interval, TimeWindow)
from canopsis.common.utils import ensure_iterable
from canopsis.task.core import get_task

from canopsis.event.manager import Event
from canopsis.check import Check

from canopsis.alerts.status import get_last_state, get_last_status, OFF

from time import time


CONF_PATH = 'alerts/manager.conf'
CATEGORY = 'ALERTS'
CONTENT = [
    Parameter('extra_fields', Parameter.array())
]


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class Alerts(MiddlewareRegistry):
    """
    Alarm cycle managment.

    Used to archive events related to alarms in a TimedStorage.
    """

    CONFIG_STORAGE = 'config_storage'
    ALARM_STORAGE = 'alarm_storage'
    CONTEXT_MANAGER = 'context'

    @property
    def config(self):
        """
        Property computed from configuration storage.
        """

        if not hasattr(self, '_config'):
            self.config = None

        return self._config

    @config.setter
    def config(self, value):
        if value is None:
            value = self.load_config()

        self._config = value

    @property
    def flapping_interval(self):
        """
        Interval used to check for flapping alarm status.
        """

        return self.config.get('bagot_time', 0)

    @property
    def flapping_freq(self):
        """
        Number of alarm oscillation during flapping interval
        to consider an alarm as flapping.
        """

        return self.config.get('bagot_freq', 0)

    @property
    def flapping_persistant_steps(self):
        """
        Number of state change steps to keep in case of long term flapping.
        Most recent steps are kept.
        """

        return self.config.get('persistant_steps', 10)

    @property
    def hard_limit(self):
        """
        Maximum number of steps an alarm can have. Only alarm cancelation or
        hard limit extension are possible ways to interact with an alarm that
        has reached this point.
        """

        return self.config.get('hard_limit', 100)

    @property
    def stealthy_interval(self):
        """
        Interval used to check for stealthy alarm status.
        """

        return self.config.get('stealthy_time', 0)

    @property
    def stealthy_show_duration(self):
        """
        Interval used to check if alarm is still in stealthy status.
        """

        return self.config.get('stealthy_show', 0)

    @property
    def restore_event(self):
        """
        When alarm is restored, reset the previous status if ``True``,
        recompute status with alarm history if ``False``.
        """

        return self.config.get('restore_event', False)

    @property
    def extra_fields(self):
        """
        Array of fields to save from event in alarm.
        """

        if not hasattr(self, '_extra_fields'):
            self.extra_fields = None

        return self._extra_fields

    @extra_fields.setter
    def extra_fields(self, value):
        if value is None:
            value = []

        self._extra_fields = value

    def __init__(
        self,
        extra_fields=None,
        config_storage=None,
        alarm_storage=None,
        context=None,
        *args, **kwargs
    ):
        super(Alerts, self).__init__(*args, **kwargs)

        if extra_fields is not None:
            self.extra_fields = extra_fields

        if config_storage is not None:
            self[Alerts.CONFIG_STORAGE] = config_storage

        if alarm_storage is not None:
            self[Alerts.ALARM_STORAGE] = alarm_storage

        if context is not None:
            self[Alerts.CONTEXT_MANAGER] = context

    def load_config(self):
        value = self[Alerts.CONFIG_STORAGE].get_elements(
            query={'crecord_type': 'statusmanagement'}
        )
        return {} if not value else value[0]

    def get_alarms(
            self,
            resolved=True,
            tags=None,
            exclude_tags=None,
            timewindow=None,
            snoozed=False
    ):
        """
        Get alarms from TimedStorage.

        :param resolved: If ``True``, returns only resolved alarms, else
                         returns only unresolved alarms (default: ``True``).
        :type resolved: bool

        :param tags: Tags which must be set on alarm (optional)
        :type tags: str or list

        :param exclude_tags: Tags which must not be set on alarm (optional)
        :type tags: str or list

        :param timewindow: Time Window used for fetching (optional)
        :type timewindow: canopsis.timeserie.timewindow.TimeWindow

        :param snoozed: If ``False``, return all non-snoozed alarms, else
                        returns alarms even if they are snoozed.
        :type snoozed: bool

        :returns: Iterable of alarms matching
        """

        query = {}

        if resolved:
            query['resolved'] = {'$ne': None}

        else:
            query['resolved'] = None

        tags_cond = None

        if tags is not None:
            tags_cond = {'$all': ensure_iterable(tags)}

        notags_cond = None

        if exclude_tags is not None:
            notags_cond = {'$not': {'$all': ensure_iterable(exclude_tags)}}

        if tags_cond is None and notags_cond is not None:
            query['tags'] = notags_cond

        elif tags_cond is not None and notags_cond is None:
            query['tags'] = tags_cond

        elif tags_cond is not None and notags_cond is not None:
            query = {'$and': [
                query,
                {'tags': tags_cond},
                {'tags': notags_cond}
            ]}

        if not snoozed:
            no_snooze_cond = {'$or': [
                    {'snooze': None},
                    {'snooze.val': {'$lte': int(time())}}
                ]
            }
            query = {'$and': [query, no_snooze_cond]}

        alarms_by_entity = self[Alerts.ALARM_STORAGE].find(
            _filter=query,
            timewindow=timewindow
        )

        cm = Context()
        for entity_id, alarms in alarms_by_entity.items():
            entity = cm.get_entity_by_id(entity_id)
            entity['entity_id'] = entity_id
            for alarm in alarms:
                alarm['entity'] = entity

        return alarms_by_entity

    def count_alarms_by_period(
            self,
            start,
            stop,
            subperiod={'day': 1},
            limit=100,
            query={},
    ):
        """
        Count alarms that have been opened during (stop - start) period.

        :param start: Beginning timestamp of period
        :type start: int

        :param stop: End timestamp of period
        :type stop: int

        :param subperiod: Cut (stop - start) in ``subperiod`` subperiods
        :type subperiod: dict

        :param limit: Counts cannot exceed this value
        :type limit: int

        :param query: Custom mongodb filter for alarms
        :type query: dict

        :return: List in which each item contains an interval and the
                 related count
        :rtype: list
        """

        intervals = Interval.get_intervals_by_period(start, stop, subperiod)

        results = []
        for date in intervals:
            count = self[Alerts.ALARM_STORAGE].count(
                data_ids=None,
                timewindow=TimeWindow(start=date['begin'], stop=date['end']),
                window_start_bind=True,
                _filter=query,
            )

            results.append(
                {
                    'date': date,
                    'count': limit if count > limit else count,
                }
            )

        return results

    def get_current_alarm(self, alarm_id):
        """
        Get current unresolved alarm.

        :param alarm_id: Alarm entity ID
        :type alarm_id: str

        :returns: Alarm as dict if found, else None
        """

        storage = self[Alerts.ALARM_STORAGE]

        result = storage.get(
            alarm_id,
            timewindow=get_offset_timewindow(),
            _filter={
                'resolved': None
            },
            limit=1
        )

        if result is not None:
            result = result[0]
            result[storage.DATA_ID] = alarm_id

        return result

    def update_current_alarm(self, alarm, new_value, tags=None):
        """
        Update alarm's history and tags.

        :param alarm: Alarm to update
        :type alarm: dict

        :param new_value: New history to set on alarm
        :type new_value: dict

        :param tags: Tags to add on alarm (optional)
        :type tags: str or list
        """

        storage = self[Alerts.ALARM_STORAGE]

        alarm_id = alarm[storage.DATA_ID]
        alarm_ts = alarm[storage.TIMESTAMP]

        if tags is not None:
            for tag in ensure_iterable(tags):
                if tag not in new_value['tags']:
                    new_value['tags'].append(tag)

        storage.put(alarm_id, new_value, alarm_ts)

    def get_events(self, alarm):
        """
        Rebuild events from alarm history.

        :param alarm: Alarm to use for events reconstruction
        :type alarm: dict

        :returns: Array of events
        """

        storage = self[Alerts.ALARM_STORAGE]
        alarm_id = alarm[storage.DATA_ID]
        alarm = alarm[storage.VALUE]

        entity = self[Alerts.CONTEXT_MANAGER].get_entity_by_id(alarm_id)

        no_author_types = ['stateinc', 'statedec', 'statusinc', 'statusdec']
        check_referer_types = [
            'ack', 'ackremove',
            'cancel', 'uncancel',
            'declareticket',
            'assocticket',
            'changestate'
        ]

        typemap = {
            'stateinc': Check.EVENT_TYPE,
            'statedec': Check.EVENT_TYPE,
            'statusinc': Check.EVENT_TYPE,
            'statusdec': Check.EVENT_TYPE,
            'ack': 'ack',
            'ackremove': 'ackremove',
            'cancel': 'cancel',
            'uncancel': 'uncancel',
            'declareticket': 'declareticket',
            'assocticket': 'assocticket',
            'changestate': 'changestate',
            'snooze': 'snooze'
        }
        valmap = {
            'stateinc': Check.STATE,
            'statedec': Check.STATE,
            'changestate': Check.STATE,
            'statusinc': Check.STATUS,
            'statusdec': Check.STATUS,
            'assocticket': 'ticket',
            'snooze': 'duration'
        }

        events = []
        eventmodel = self[Alerts.CONTEXT_MANAGER].get_event(entity)

        for step in alarm['steps']:
            event = eventmodel.copy()
            event['timestamp'] = step['t']
            event['output'] = step['m']

            if step['_t'] in valmap:
                field = valmap[step['_t']]
                event[field] = step['val']

            if step['_t'] not in no_author_types:
                event['author'] = step['a']

            if step['_t'] in check_referer_types:
                event['event_type'] = 'check'
                event['ref_rk'] = Event.get_rk(event)

            if Check.STATE not in event:
                event[Check.STATE] = get_last_state(alarm)

            event['event_type'] = typemap[step['_t']]

            for field in self.extra_fields:
                if field in alarm['extra']:
                    event[field] = alarm['extra'][field]

            events.append(event)

        return events

    def archive(self, event):
        """
        Archive event in corresponding alarm history.

        :param event: Event to archive
        :type event: dict
        """

        entity = self[Alerts.CONTEXT_MANAGER].get_entity(event)
        entity_id = self[Alerts.CONTEXT_MANAGER].get_entity_id(entity)

        author = event.get('author', None)
        message = event.get('output', None)

        if event['event_type'] == Check.EVENT_TYPE:
            alarm = self.get_current_alarm(entity_id)

            if alarm is None:
                if event[Check.STATE] == Check.OK:
                    # If a check event with an OK state concerns an entity for
                    # which no alarm is opened, there is no point continuing
                    return

                # Check is not OK
                alarm = self.make_alarm(entity_id, event)
                alarm = self.update_state(alarm, event[Check.STATE], event)

            else:  # Alarm is already opened
                value = alarm.get(self[Alerts.ALARM_STORAGE].VALUE)
                if self.is_hard_limit_reached(value):
                    return

                alarm = self.update_state(alarm, event[Check.STATE], event)

            value = alarm.get(self[Alerts.ALARM_STORAGE].VALUE)

            value = self.crop_flapping_steps(value)

            value = self.check_hard_limit(value)

            self.update_current_alarm(alarm, value)

        else:
            try:
                task = get_task('alerts.useraction.{0}'.format(
                    event['event_type']
                ), cacheonly=True)

            except ImportError:
                task = None

            if task is not None:
                alarm = self.get_current_alarm(entity_id)
                if alarm is None:
                    self.logger.warning(
                        'Entity {} has no current alarm : ignoring'.format(
                            entity_id
                        )
                    )
                    return

                value = alarm.get(self[Alerts.ALARM_STORAGE].VALUE)

                if self.is_hard_limit_reached(value):
                    # Only cancel is allowed when hard limit has been reached
                    if event['event_type'] != 'cancel':
                        return

                new_value = task(self, value, author, message, event)
                status = None

                if isinstance(new_value, tuple):
                    new_value, status = new_value

                new_value = self.check_hard_limit(new_value)

                self.update_current_alarm(alarm, new_value)

                if status is not None:
                    alarm = self.update_status(alarm, status, event)
                    new_value = alarm[self[Alerts.ALARM_STORAGE].VALUE]

                    self.update_current_alarm(alarm, new_value)

    def update_state(self, alarm, state, event):
        """
        Update alarm state if needed.

        :param alarm: Alarm associated to state change event
        :type alarm: dict

        :param state: New state to archive
        :type state: int

        :param event: Associated event
        :type event: dict

        :return: updated alarm
        :rtype: dict
        """

        value = alarm.get(self[Alerts.ALARM_STORAGE].VALUE)

        old_state = get_last_state(value, ts=event['timestamp'])

        if state != old_state:
            return self.change_of_state(alarm, old_state, state, event)

        return alarm

    def update_status(self, alarm, status, event):
        """
        Update alarm status if needed.

        :param alarm: Alarm associated to status change event
        :type alarm: dict

        :param status: New status to archive
        :type status: int

        :param event: Associated event
        :type event: dict

        :return: updated alarm
        :rtype: dict
        """

        value = alarm.get(self[Alerts.ALARM_STORAGE].VALUE)

        old_status = get_last_status(value, ts=event['timestamp'])

        if status != old_status:
            return self.change_of_status(
                alarm,
                old_status,
                status,
                event
            )

        return alarm

    def change_of_state(self, alarm, old_state, state, event):
        """
        Change state when ``update_state()`` detected a state change.

        :param alarm: Associated alarm to state change event
        :type alarm: dict

        :param old_state: Previous state
        :type old_state: int

        :param state: New state
        :type state: int

        :param event: Associated event
        :type event: dict

        :return: alarm with changed state
        :rtype: dict
        """

        if state > old_state:
            task = get_task(
                'alerts.systemaction.state_increase', cacheonly=True
            )

        elif state < old_state:
            task = get_task(
                'alerts.systemaction.state_decrease', cacheonly=True
            )

        value = alarm.get(self[Alerts.ALARM_STORAGE].VALUE)
        new_value, status = task(self, value, state, event)

        alarm[self[Alerts.ALARM_STORAGE].VALUE] = new_value

        return self.update_status(alarm, status, event)

    def change_of_status(self, alarm, old_status, status, event):
        """
        Change status when ``update_status()`` detected a status
        change.

        :param alarm: Associated alarm to status change event
        :type alarm: dict

        :param old_status: Previous status
        :type old_status: int

        :param status: New status
        :type status: int

        :param event: Associated event
        :type event: dict

        :return: alarm with changed status
        :rtype: dict
        """

        if status > old_status:
            task = get_task(
                'alerts.systemaction.status_increase', cacheonly=True
            )

        elif status < old_status:
            task = get_task(
                'alerts.systemaction.status_decrease', cacheonly=True
            )

        value = alarm.get(self[Alerts.ALARM_STORAGE].VALUE)
        new_value = task(self, value, status, event)

        alarm[self[Alerts.ALARM_STORAGE].VALUE] = new_value

        return alarm

    def make_alarm(self, alarm_id, event):
        """
        Create a new alarm from event if not already existing.

        :param alarm_id: Alarm entity ID
        :type alarm_id: str

        :param event: Associated event
        :type event: dict

        :return alarm document:
        :rtype: dict
        """

        return {
            self[Alerts.ALARM_STORAGE].DATA_ID: alarm_id,
            self[Alerts.ALARM_STORAGE].TIMESTAMP: event['timestamp'],
            self[Alerts.ALARM_STORAGE].VALUE: {
                'state': None,
                'status': None,
                'ack': None,
                'canceled': None,
                'snooze': None,
                'hard_limit': None,
                'ticket': None,
                'resolved': None,
                'steps': [],
                'tags': [],
                'extra': {
                    field: event[field]
                    for field in self.extra_fields
                    if field in event
                }
            }
        }

    def crop_flapping_steps(self, alarm):
        """
        Remove old state changes for alarms that are flapping over long periods
        of time.

        :param dict alarm: Alarm value

        :return: Alarm with cropped steps or alarm if nothing to remove
        :rtype: dict
        """

        p_steps = self.flapping_persistant_steps

        if p_steps < 0:
            self.logger.warning(
                "Peristant steps is {} (< 0) : aborting flapping steps crop "
                "operation".format(p_steps)
            )
            return alarm

        last_status_i = alarm['steps'].index(alarm['status'])

        state_changes = filter(
            lambda step: step['_t'] in ['stateinc', 'statedec'],
            alarm['steps'][last_status_i + 1:]
        )

        number_to_crop = len(state_changes) - p_steps

        if not number_to_crop > 0:
            return alarm

        crop_counter = {}

        # Removed steps are supposed unique due to their timestamps, so as
        # `remove` method does not cause any collisions.
        for i in range(number_to_crop):
            # Increase statedec or stateinc counter
            t = state_changes[i]['_t']
            crop_counter[t] = crop_counter.get(t, 0) + 1

            # Increase {0,1,2,3} counter
            s = 'state:{}'.format(state_changes[i]['val'])
            crop_counter[s] = crop_counter.get(s, 0) + 1

            alarm['steps'].remove(state_changes[i])

        task = get_task('alerts.systemaction.update_state_counter')
        alarm = task(alarm, crop_counter)

        return alarm

    def is_hard_limit_reached(self, alarm):
        """
        Check if an hard limit is on going.

        :param dict alarm: Alarm value

        :return: False if hard_limit property is None or if configured value is
          greater than recorded value, True otherwise
        :rtype: boolean
        """

        limit = alarm.get('hard_limit', None)

        if limit is None:
            return False

        if limit['val'] < self.hard_limit:
            return False

        return True

    def check_hard_limit(self, alarm):
        """
        Update hard limit informations if number of steps has exceeded this
        limit.

        :param dict alarm: Alarm value

        :return: Alarm with hard limit informations or alarm if nothing to do
        :rtype: dict
        """

        limit = alarm.get('hard_limit', None)

        if limit is not None:
            if limit['val'] >= self.hard_limit:
                return alarm

        if len(alarm['steps']) >= self.hard_limit:
            task = get_task('alerts.systemaction.hard_limit')
            return task(self, alarm)

        else:
            return alarm

    def resolve_alarms(self):
        """
        Loop over all unresolved alarms, and check if it can be resolved.
        """

        storage = self[Alerts.ALARM_STORAGE]
        result = self.get_alarms(resolved=False)

        for data_id in result:
            for docalarm in result[data_id]:
                docalarm[storage.DATA_ID] = data_id
                alarm = docalarm.get(storage.VALUE)

                if get_last_status(alarm) == OFF:
                    t = alarm['status']['t']
                    now = int(time())

                    if (now - t) > self.flapping_interval:
                        alarm['resolved'] = t
                        self.update_current_alarm(docalarm, alarm)
