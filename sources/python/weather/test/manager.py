#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
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

from canopsis.weather.manager import Weather


class TestManager(TestCase):
    def setUp(self):
        self.wm = Weather()

        # Calling this value will set it for the first time
        self.wm.weather_aggr

    def test_context_entities_aggr(self):
        f = {'field': 'value'}
        l = 100

        res = self.wm.context_entities_aggr(filter_=f, limit=l)

        expected = [
            {
                '$match': f
            },
            {
                '$limit': l
            }
        ]

        self.assertEqual(res, expected)

    def test_alarm_lookup_aggr(self):
        res = self.wm.alarm_lookup_aggr()

        expected = [
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

        self.assertEqual(res, expected)

    def test_linklist_lookup_aggr(self):
        res = self.wm.linklist_lookup_aggr()

        expected = [
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

        self.assertEqual(res, expected)

    def test_pbehaviors_lookup_aggr(self):
        res = self.wm.pbehaviors_lookup_aggr()

        expected = [
            {
                '$lookup': {
                    'from': 'default_pbehavior',
                    'localField': 'entity_id',
                    'foreignField': 'eids',
                    'as': 'pbehaviors'
                }
            }
        ]

        self.assertEqual(res, expected)

    def test_lookups_aggr(self):
        cases = [
            {
                'lookups': [],
                'expected_count': 0
            },
            {
                'lookups': ['alarm'],
                'expected_count': 2
            },
            {
                'lookups': ['alarm', 'linklist', 'pbehaviors'],
                'expected_count': 5
            },
            {
                'lookups': ['alarm', 'unknown_aggr'],
                'expected_count': 2
            },
            {
                'lookups': ['unknown_aggr'],
                'expected_count': 0
            }
        ]

        for case in cases:
            self.wm._weather_aggr['lookups'] = case['lookups']

            lookups = self.wm.lookups_aggr()
            self.assertEqual(len(lookups), case['expected_count'])

    def test_weather_projection_aggr(self):
        cases = [
            {
            },
            {
                'a': 1
            },
            {
                'a': 1,
                'b': '$hey.ho.hey'
            }
        ]

        for case in cases:
            self.wm._weather_aggr['ui_projection'] = case

            res = self.wm.weather_projection_aggr()
            expected = [{'$project': case}]

            self.assertEqual(res, expected)

    def test_sort_aggr(self):
        res = self.wm.sort_aggr('key', 'ASC')
        self.assertEqual(res, [{'$sort': {'key': 1}}])

        res = self.wm.sort_aggr('other_key', 'DESC')
        self.assertEqual(res, [{'$sort': {'other_key': -1}}])

        with self.assertRaises(ValueError):
            self.wm.sort_aggr('key', 'WRONG')

    def test_get_entities(self):
        self.assertEqual(self.wm.get_entities('/my/entity'), [])

    def test_get_weather(self):
        self.wm.get_weather(filter_={'my': 'filter'})


if __name__ == '__main__':
    main()
