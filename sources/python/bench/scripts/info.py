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


from re import sub

"""
script to get architecture's informations
"""

file_meminfo = open('/proc/meminfo', 'r')
file_cpuinfo = open('/proc/cpuinfo', 'r')
file_conf = open('../etc/bench/bench.conf', 'w')

memory = ''
cpu_name = []
cadence = ''

for line in file_meminfo:
    linesplitted = line.split(':')
    if linesplitted[0] == 'MemTotal':
        memory = linesplitted[1]

for line in file_cpuinfo:
    linesplitted = line.split(':')
    if linesplitted[0] == 'model name\t':
        cpu_name = linesplitted[1].split(' ')

cadence = cpu_name[len(cpu_name) - 1]

memory = sub(r'[a-z     :A-Z\n]', '', memory)
cadence = sub(r'[a-z     :A-Z\n]', '', cadence)

file_conf.write('[BENCH]\n\nmemory={0}\ncadence={1}\nbenchmode=True'.format(
                memory,
                cadence
                ))


file_meminfo.close()
file_cpuinfo.close()
file_conf.close()
