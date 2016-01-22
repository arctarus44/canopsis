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

from canopsis.collectd.utils import types
from canopsis.task.core import register_task
from canopsis.event.base import Event
import re


@register_task
def event_processing(engine, event, logger=None, **kwargs):
    prog = re.compile(
        '^(PUTVAL) ("(.+)"|([^\s]+)) (interval=.+) ([^\s]+)$'
    )

    match = re.match(prog, event)

    if match:
        action = match.group(1)
        cnode = match.group(3 if match.group(3) else 4).split('/')
        options = match.group(5)
        values = match.group(6).split(':')

        logger.debug('action={0}'.format(action))
        logger.debug('options={0}'.format(options))

        if action == 'PUTVAL':
            component = cnode[0]
            resource = cnode[1]
            metric = cnode[2]

            ctype = types.get(metric, None)

            if ctype is None:
                ctypename, metric = metric.split('-', 1)
                ctype = types.get(ctypename, None)

            if ctype is None:
                logger.error('Invalid format: {0}'.format(event))
                return None

            try:
                ts = int(float(values[0]))

            except ValueError as err:
                logger.error('Invalid timestamp: {0}'.format(err))
                return None

            values = values[1:]

            logger.debug('values={0}'.format(values))
            logger.debug('ctype={0}'.format(ctype))

            logger.debug('timestamp={0}'.format(ts))
            logger.debug('component={0}'.format(component))
            logger.debug('resource={0}'.format(resource))
            logger.debug('metric={0}'.format(metric))

            metrics = []
            i = 0

            for value in values:
                name = ctype[i]['name']
                unit = ctype[i]['unit']
                vmin = ctype[i]['min']
                vmax = ctype[i]['max']
                dtype = ctype[i]['type']

                if vmin == 'U':
                    vmin = None

                if vmax == 'U':
                    vmax = None

                if name == "value":
                    name = metric

                if metric != name:
                    name = "{0}-{1}".format(metric, name)

                try:
                    value = float(value)

                except ValueError as err:
                    logger.error('Invalid value {0}: {1}'.format(value, err))

                else:
                    logger.debug('name={0}'.format(name))
                    logger.debug('point: {0} ({1})'.format(value, dtype))

                    metrics.append({
                        'metric': name,
                        'value': value,
                        'unit': unit,
                        'min': vmin,
                        'max': vmax,
                        'type': dtype
                    })

                i += 1

            event = Event.create(
                timestamp=ts,
                connector='collectd',
                connector_name='collectd2event',
                event_type='perf',
                source_type='resource',
                component=component,
                resource=resource,
                metrics=metrics
            )

            publisher = engine[engine.MOM].get_publisher()
            publisher(event)
