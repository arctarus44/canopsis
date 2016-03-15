# -*- coding: utf-8 -*-

from canopsis.middleware.registry import MiddlewareRegistery

CONF_PATh = 'bench/manager.conf'
CATEGORY = 'BENCH'


class Bench(MiddlewareRegistery):
    """
    bench storage
    """

    NAME = 'bench'

    STORAGE = 'bench_storage'
