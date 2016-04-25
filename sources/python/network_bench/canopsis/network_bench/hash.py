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

from __future__ import unicode_literals
from collections import Hashable


class HashGenerator(object):

    def __init__(self, *args, **kwargs):
        super(HashGenerator, self).__init__(*args, **kwargs)

    def dict_to_unicode(self, dic):

        keys = []

        for key, value in dic.items():
            if not isinstance(key, unicode):
                keys.append(key)
            if isinstance(value, str):
                dic[key] = unicode(value, 'utf-8')

        for key in keys:
            tmp = unicode(key, 'utf_8')
            dic[tmp] = dic.pop(key)

        return dic

    def get_hash(self, message):

        if isinstance(message, Hashable):

            return hash(message)

        elif isinstance(message, dict):
            try:
                message.pop('rk')
            except:
                pass

            try:
                message.pop(u'rk')
            except:
                pass

            dict_tmp = self.dict_to_unicode(message)

            file = open('/home/tgosselin/fichierdelog2', 'a')
            file.write('dico a hash: {0}\n'.format(dict_tmp))
            file.close()

            listtosort = []
            for name in dict_tmp:
                val = dict_tmp[name]

                if isinstance(val, Hashable):
                    listtosort.append((name, val))
                else:
                    listtosort.append((name, self.get_hash(val)))

            listtosort.sort(key=lambda x: x[0])
            result = listtosort

            return hash(str(result))

        elif isinstance(message, list):

            counter = 0

            for i in message:
                if not isinstance(i, Hashable):
                    message[counter] = self.get_hash(i)
                counter += 1

            message.sort()

            return hash(str(message))

        else:

            return message
