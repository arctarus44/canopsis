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

from utils import Singleton
from time import sleep
from threading import Thread


class Publisher(object):

    """
    this class publish engine's benchs results
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.list = []
        timer = ThreadTimer(self)
        timer.start()

    def addList(self, list):
        inList = self.inList(list)
        if inList != -1:
            self.list[inList] = self.average(inList, list)
        else:
            self.list.append(list)

    def inList(self, list):
        for i in list:
            if list[0] == self.list[i][0]:
                return i
        return -1

    def averageValues(self, dic1, dic2):
        newValue = (dic1.get('value') + dic2.get('value')) / 2
        new = {
            'value': newValue
        }
        return dic1.update(new)

    def average(self, i, list):
        newList = []
        newList.append(list[0])
        newList.append(self.averageValues(self.list[1], list[1]))
        newList.append(self.averageValues(self.list[2], list[2]))
        newList.append(self.averageValues(self.list[3], list[3]))
        return newList

    def cleanList(self):
        self.list = []

    def publish(self):
        # publish list
        pass


class ThreadTimer(Thread):

    def __init__(self, publisher):
        super(ThreadTimer, self).__init__()
        self.publisher = publisher

    def run(self):
        while True:
            sleep(60)
            self.publisher.publish()
            self.publisher.cleanList()
