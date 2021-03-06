#!/usr/bin/env python
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

from unittest import TestCase, main

from canopsis.middleware.core import Middleware
from canopsis.check import Check

from canopsis.alerts.manager import Alerts
from canopsis.alerts.status import (
    ONGOING, CANCELED, OFF,
    is_flapping, is_stealthy, compute_status, get_last_state, get_last_status,
    get_previous_step
)


class TestStatus(TestCase):
    def setUp(self):
        self.alarm_storage = Middleware.get_middleware_by_uri(
            'storage-periodical-testalarm://'
        )
        self.config_storage = Middleware.get_middleware_by_uri(
            'storage-default-testconfig://'
        )

        self.manager = Alerts()
        self.manager[Alerts.ALARM_STORAGE] = self.alarm_storage
        self.manager[Alerts.CONFIG_STORAGE] = self.config_storage

        self.config_storage.put_element(
            element={
                '_id': 'test_config',
                'crecord_type': 'statusmanagement',
                'bagot_time': 3600,
                'bagot_freq': 10,
                'stealthy_time': 300,
                'stealthy_show': 600,
                'restore_event': True
            },
            _id='test_config'
        )

        self.alarm = {
            'state': None,
            'status': None,
            'ack': None,
            'canceled': None,
            'ticket': None,
            'resolved': None,
            'steps': [],
            'tags': []
        }

    def test_is_flapping(self):
        self.alarm['steps'] = [
            {
                '_t': 'stateinc',
                't': 0,
                'a': 'test',
                'm': 'test',
                'val': Check.CRITICAL
            },
            {
                '_t': 'statedec',
                't': 1,
                'a': 'test',
                'm': 'test',
                'val': Check.OK
            },
            {
                '_t': 'stateinc',
                't': 2,
                'a': 'test',
                'm': 'test',
                'val': Check.CRITICAL
            },
            {
                '_t': 'statedec',
                't': 3,
                'a': 'test',
                'm': 'test',
                'val': Check.OK
            },
            {
                '_t': 'stateinc',
                't': 4,
                'a': 'test',
                'm': 'test',
                'val': Check.CRITICAL
            },
            {
                '_t': 'statedec',
                't': 5,
                'a': 'test',
                'm': 'test',
                'val': Check.OK
            },
            {
                '_t': 'stateinc',
                't': 6,
                'a': 'test',
                'm': 'test',
                'val': Check.CRITICAL
            },
            {
                '_t': 'statedec',
                't': 7,
                'a': 'test',
                'm': 'test',
                'val': Check.OK
            },
            {
                '_t': 'stateinc',
                't': 8,
                'a': 'test',
                'm': 'test',
                'val': Check.CRITICAL
            },
            {
                '_t': 'statedec',
                't': 9,
                'a': 'test',
                'm': 'test',
                'val': Check.OK
            },
            {
                '_t': 'stateinc',
                't': 10,
                'a': 'test',
                'm': 'test',
                'val': Check.CRITICAL
            },
        ]

        self.alarm['state'] = self.alarm['steps'][-1]

        got = is_flapping(self.manager, self.alarm)
        self.assertTrue(got)

    def test_isnot_flapping(self):
        self.alarm['steps'] = [
            {
                '_t': 'stateinc',
                't': 0,
                'a': 'test',
                'm': 'test',
                'val': Check.CRITICAL
            },
            {
                '_t': 'statedec',
                't': 1,
                'a': 'test',
                'm': 'test',
                'val': Check.OK
            }
        ]

        self.alarm['state'] = self.alarm['steps'][-1]

        got = is_flapping(self.manager, self.alarm)
        self.assertFalse(got)

    def test_is_stealthy(self):
        self.alarm['steps'].append({
            '_t': 'stateinc',
            't': 0,
            'a': 'test',
            'm': 'test',
            'val': Check.CRITICAL
        })
        self.alarm['state'] = {
            '_t': 'statedec',
            't': 1,
            'a': 'test',
            'm': 'test',
            'val': Check.OK
        }

        got = is_stealthy(self.manager, self.alarm)

        self.assertTrue(got)

    def test_isnot_stealthy(self):
        self.alarm['steps'].append({
            '_t': 'stateinc',
            't': 0,
            'a': 'test',
            'm': 'test',
            'val': Check.CRITICAL
        })
        self.alarm['state'] = {
            '_t': 'statedec',
            't': 601,
            'a': 'test',
            'm': 'test',
            'val': Check.OK
        }

        got = is_stealthy(self.manager, self.alarm)

        self.assertFalse(got)

    def test_is_ongoing(self):
        self.alarm['state'] = {
            '_t': 'stateinc',
            't': 0,
            'a': 'test',
            'm': 'test',
            'val': Check.CRITICAL
        }
        got = compute_status(self.manager, self.alarm)
        self.assertEqual(got, ONGOING)

    def test_is_canceled(self):
        self.alarm['canceled'] = {
            '_t': 'cancel',
            't': 0,
            'a': 'test',
            'm': 'test'
        }
        got = compute_status(self.manager, self.alarm)
        self.assertEqual(got, CANCELED)

    def test_is_off(self):
        self.alarm['state'] = {
            '_t': 'statedec',
            't': 0,
            'a': 'test',
            'm': 'test',
            'val': Check.OK
        }
        got = compute_status(self.manager, self.alarm)
        self.assertEqual(got, OFF)

    def test_get_last_state(self):
        got = get_last_state(self.alarm)
        self.assertEqual(got, Check.OK)

        self.alarm['state'] = {
            '_t': 'stateinc',
            't': 0,
            'a': 'test',
            'm': 'test',
            'val': Check.CRITICAL
        }

        got = get_last_state(self.alarm)
        self.assertEqual(got, Check.CRITICAL)

    def test_get_last_status(self):
        got = get_last_status(self.alarm)
        self.assertEqual(got, OFF)

        self.alarm['status'] = {
            '_t': 'statusinc',
            't': 0,
            'a': 'test',
            'm': 'test',
            'val': ONGOING
        }

        got = get_last_status(self.alarm)
        self.assertEqual(got, ONGOING)

    def test_get_previous_step(self):
        expected = {
            '_t': 'teststep',
            't': 0,
            'a': 'test',
            'm': 'test'
        }
        self.alarm['steps'].append(expected)

        step = get_previous_step(self.alarm, 'teststep')

        self.assertTrue(expected is step)


if __name__ == '__main__':
    main()
