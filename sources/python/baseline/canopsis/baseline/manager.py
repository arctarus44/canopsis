# -*- coding: utf-8 -*-

from time import time

from canopsis.middleware.registry import MiddlewareRegistry
from b3j0f.conf import Configurable

@Configurable(paths='baseline/manager.conf')
class Baseline(MiddlewareRegistry):
    """Baseline"""

    
