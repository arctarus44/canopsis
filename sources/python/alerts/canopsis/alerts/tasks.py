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

from canopsis.alerts.status import compute_status
from canopsis.task.core import register_task
from canopsis.alerts import status


@register_task('alerts.useraction.ack')
def acknowledge(manager, alarm, author, message, event):
    step = {
        '_t': 'ack',
        't': event['timestamp'],
        'a': author,
        'm': message
    }

    alarm['ack'] = step
    alarm['steps'].append(step)

    return alarm


@register_task('alerts.useraction.ackremove')
def unacknowledge(manager, alarm, author, message, event):
    step = {
        '_t': 'ackremove',
        't': event['timestamp'],
        'a': author,
        'm': message
    }

    alarm['ack'] = None
    alarm['steps'].append(step)

    return alarm


@register_task('alerts.useraction.cancel')
def cancel(manager, alarm, author, message, event):
    step = {
        '_t': 'cancel',
        't': event['timestamp'],
        'a': author,
        'm': message
    }

    alarm['canceled'] = step
    alarm['steps'].append(step)

    return alarm, status.CANCELED


@register_task('alerts.useraction.uncancel')
def restore(manager, alarm, author, message, event):
    step = {
        '_t': 'uncancel',
        't': event['timestamp'],
        'a': author,
        'm': message
    }

    canceled = alarm['canceled']
    alarm['canceled'] = None
    alarm['steps'].append(step)

    status = None

    if manager.restore_event:
        status = status.get_last_status(alarm, ts=canceled['t'])

    else:
        status = status.compute_status(alarm)

    return alarm, status


@register_task('alerts.useraction.declareticket')
def declare_ticket(manager, alarm, author, message, event):
    step = {
        '_t': 'declareticket',
        't': event['timestamp'],
        'a': author,
        'm': message,
        'val': None
    }

    alarm['ticket'] = step
    alarm['steps'].append(step)

    return alarm


@register_task('alerts.useraction.assocticket')
def associate_ticket(manager, alarm, author, message, event):
    step = {
        '_t': 'assocticket',
        't': event['timestamp'],
        'a': author,
        'm': message,
        'val': event['ticket']
    }

    alarm['ticket'] = step
    alarm['steps'].append(step)

    return alarm


@register_task('alerts.useraction.changestate')
def change_state(manager, alarm, author, message, event):
    step = {
        '_t': 'changestate',
        't': event['timestamp'],
        'a': author,
        'm': message,
        'val': event['state']
    }

    alarm['state'] = step
    alarm['steps'].append(step)

    return alarm


@register_task('alerts.systemaction.state_increase')
def state_increase(manager, alarm, state, event):
    step = {
        '_t': 'stateinc',
        't': event['timestamp'],
        'a': '{0}.{1}'.format(event['connector'], event['connector_name']),
        'm': event['output'],
        'val': state
    }

    if alarm['state'] is None or alarm['state']['_t'] != 'changestate':
        alarm['state'] = step

    status = compute_status(manager, alarm)
    alarm['steps'].append(step)

    return alarm, status


@register_task('alerts.systemaction.state_decrease')
def state_decrease(manager, alarm, state, event):
    step = {
        '_t': 'statedec',
        't': event['timestamp'],
        'a': '{0}.{1}'.format(event['connector'], event['connector_name']),
        'm': event['output'],
        'val': state
    }

    if alarm['state'] is None or alarm['state']['_t'] != 'changestate':
        alarm['state'] = step

    status = compute_status(manager, alarm)
    alarm['steps'].append(step)

    return alarm, status


@register_task('alerts.systemaction.status_increase')
def status_increase(manager, alarm, status, event):
    step = {
        '_t': 'statusinc',
        't': event['timestamp'],
        'a': '{0}.{1}'.format(event['connector'], event['connector_name']),
        'm': event['output'],
        'val': status
    }

    alarm['steps'].append(step)

    return alarm


@register_task('alerts.systemaction.status_decrease')
def status_decrease(manager, alarm, status, event):
    step = {
        '_t': 'statusdec',
        't': event['timestamp'],
        'a': '{0}.{1}'.format(event['connector'], event['connector_name']),
        'm': event['output'],
        'val': status
    }

    if status == status.OFF:
        alarm['resolved'] = step['t']

    alarm['steps'].append(step)

    return alarm
