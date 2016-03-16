# -*- coding: utf-8 -*-

from canopsis.middleware.registry import MiddlewareRegistery

CONF_PATh = 'bench/manager.conf'
CATEGORY = 'BENCH'


class BenchManager(MiddlewareRegistery):

    """
    bench storage
    """

    NAME = 'bench'
    STORAGE = 'bench_storage'

    def __init__(self, *args, **kwargs):
        super(BenchManager, self).__init__(*args, **kwargs)

    def put(self):
        self.[BenchManager.bench_storage].put(
        	
        )
