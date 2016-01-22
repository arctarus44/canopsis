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

from canopsis.middleware.registry import MiddlewareRegistry
from canopsis.configuration.configurable import conf_paths
from canopsis.configuration.configurable import add_category

from dateutil.rrule import rrulestr
from datetime import datetime
from time import time


CONF_PATH = 'scheduledjobs/manager.conf'
CATEGORY = 'JOBMANAGER'
CONTENT = []


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class JobManager(MiddlewareRegistry):

    JOB_STORAGE = 'job_storage'
    MOM = 'mom'

    def __init__(self, job_storage=None, mom=None, *args, **kwargs):
        super(JobManager, self).__init__(*args, **kwargs)

        if job_storage is not None:
            self[JobManager.JOB_STORAGE] = job_storage

        if mom is not None:
            self[JobManager.MOM] = mom

        self.last_pending_fetch = 0

    def execute(self, job, context=None):
        storage = self[JobManager.JOB_STORAGE]

        if isinstance(job, basestring):
            job = storage.get_elements(ids=job)

        if job is None:
            self.logger.error('No job provided')
            return

        job['params']['jobid'] = job[storage.DATA_ID]
        job['params']['jobctx'] = context if context is not None else {}

        publisher = self[JobManager.MOM].get_publisher(job['task'])
        publisher(job['params'])

    def get_pending_jobs(self):
        storage = self[JobManager.JOB_STORAGE]

        now = time()
        prev = now - self.last_pending_fetch
        self.last_pending_fetch = now

        jobs = storage.find_elements(
            query={'$and': [
                {'$or': [
                    {'jtype': {'$exists': False}},
                    {'jtype': None},
                    {'jtype': 'scheduled'}
                ]},
                {'$or': [
                    {'last_execution': {'$lte': prev}},
                    {'last_execution': None}
                ]}
            ]}
        )

        def hastoexecjob(job):
            if job['last_execution'] <= 0:
                return True

            start = datetime.fromtimestamp(job['start'])
            dtstart = datetime.fromtimestamp(prev)
            dtend = datetime.fromtimestamp(now)

            rrule = rrulestr(job['rrule'], dtstart=start)
            occurences = list(rrule.between(dtstart, dtend))

            return len(occurences) > 0

        result = [
            job
            for job in jobs
            if hastoexecjob(job)
        ]

        self.logger.debug('Pending jobs: {0}'.format(
            [job[storage.DATA_ID] for job in result]
        ))

        return result
