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

from canopsis.timeserie.aggregation import get_aggregations
from canopsis.timeserie.timewindow import TimeWindow
from canopsis.timeserie.core import TimeSerie
from canopsis.task.core import register_task


def new_operator(op, manager, period, perfdatas):
    def operator(regex):
        points = manager.subset_perfdata_superposed(regex, perfdatas)
        result = float('nan')

        if len(points) > 0:
            ts = TimeSerie(
                period=period,
                aggregation=op,
                round_time=False
            )

            tw = TimeWindow(start=points[0][0], stop=points[-1][0])

            consolidated = ts.calculate(points, tw)

            if len(consolidated) > 0:
                result = consolidated[0][1]

        return result

    return operator


@register_task('serie.operatorset')
def serie_operatorset(manager, period, perfdatas):
    operators = {
        key: new_operator(key.lower(), manager, period, perfdatas)
        for key in get_aggregations()
    }

    return operators
