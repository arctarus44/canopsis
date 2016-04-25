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

#from kombu import Connection as AMQPConnection
#from kombu.pools import producers as AMQPProducers

#from b3j0f.conf import Configurable, Category

from time import sleep
from threading import Thread


#@Configurable(paths='network_bench/amqp.conf', conf=Category('AMQP'))
class Publisher(object):

    def __init__(
            self,
            # url='amqp://cpsrabbit:canopsis@localhost:5672/canopsis',
            *args,
            **kwargs):
        super(Publisher, self).__init__(*args, **kwargs)
        #self.url = url
        self.times = []

        print('démarrage publisher')

        self.timer = ThreadTimer(self)
        self.timer.start()

    def get_time(self, times):
        print('times before {0}\n'.format(self.times))
        self.times += times
        print('times after {0}\n'.format(self.times))


    def clean_times(self):
        self.times = []

    def gen_event(self):
        """
        event = {
            'connector': 'Times',
            'connector_name': 'times',
            'event_type': 'check',
            'source_type': 'resource',
            'resource': 'resource',
            'output': 'average: {0}'.format(self.time_average)
        }

        self.amqp_publish(event)
        """

        print('average: {0}\n'.format(
            self.time_average()))

    def time_average(self):
        print('\n{0}\n'.format(self.times))
        cnt = 0
        tmp = 0
        for i in self.times:
            cnt += 1
            tmp += float(i)

        if cnt == 0:
            return -1
        else:
            return (tmp / cnt)

    def amqp_publish(self, event):
        """
        publish an event on amqp

        :param event: an event to publish
        :return: a boolean
        """

        print('dans le publisher event: {0}\n'.format(event))
        """
        with AMQPConnection(self.url) as conn:
            with AMQPProducers[conn].acquire(block=True) as producer:
                rk = '{0}.{1}.{2}.{3}.{4}'.format(
                    event['connector'],
                    event['connector_name'],
                    event['event_type'],
                    event['source_type'],
                    event['component']
                )

                if event['source_type'] == 'resource':
                    rk = '{0}.{1}'.format(rk, event['resource'])

                producer.publish(
                    event, serializer='json',
                    exchange='canopsis.events', routing_key=rk
                )
        """

    def publish_message(self, message):

        print('dans le publisher message: {0}\n'.format(message))
        """
        event = {
            'connector': 'Message',
            'connector_name': 'message',
            'event_type': 'check',
            'source_type': 'resource',
            'resource': 'resource',
            'output': '{0}'.format(self.message)
        }

        with AMQPConnection(self.url) as conn:
            with AMQPProducers[conn].acquire(block=True) as producer:
                rk = '{0}.{1}.{2}.{3}.{4}'.format(
                    event['connector'],
                    event['connector_name'],
                    event['event_type'],
                    event['source_type'],
                    event['component']
                )

                if event['source_type'] == 'resource':
                    rk = '{0}.{1}'.format(rk, event['resource'])

                producer.publish(
                    event, serializer='json',
                    exchange='canopsis.events', routing_key=rk
                )

        """


class ThreadTimer(Thread):

    def __init__(self, publisher, *args, **kwargs):
        super(ThreadTimer, self).__init__(*args, **kwargs)
        self.publisher = publisher

    def run(self):
        while True:
            sleep(60)
            self.publisher.gen_event()
