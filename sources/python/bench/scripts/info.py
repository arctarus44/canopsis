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

"""
script to get architecture's informations
"""

file_meminfo = open('/proc/meminfo', 'r')
file_cpuinfo = open('/proc/cpuinfo', 'r')
file_conf = open('../etc/bench/architecture.conf', 'w')

memory = ''
number_of_core = 0
cpu_name = []
cadence = ''

for line in file_meminfo:
    linesplitted = line.split(':')
    if linesplitted[0] == 'MemTotal':
        memory = linesplitted[1]

for line in file_cpuinfo:
    linesplitted = line.split(':')
    if linesplitted[0] == 'processor\t':
        number_of_core += 1
    if linesplitted[0] == 'model name\t':
        cpu_name = linesplitted[1].split(' ')

cadence = cpu_name[len(cpu_name) - 1]

file_conf.write('memory: {0}number of core: {1}\ncadence: {2}'.format(
                memory,
                number_of_core,
                cadence
                ))
