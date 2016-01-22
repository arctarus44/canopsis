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

from canopsis.task.core import register_task
from canopsis.event.check import Check


def task_handler(func):
    @register_task
    def event_processing(engine, event, **params):
        try:
            func(engine=engine, job=event, **params)

        except Exception as err:
            event = Check.create(
                source_type='resource',
                component=engine.name,
                resource=event['jobid'],
                output='An error occured: {0}'.format(err),
                state=Check.CRITICAL
            )

        else:
            event = Check.create(
                source_type='resource',
                component=engine.name,
                resource=event['jobid'],
                output='OK',
                state=Check.INFO
            )

        publisher = engine[engine.MOM].get_publisher()
        publisher(event)

    return event_processing
