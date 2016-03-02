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

from canopsis.configuration.configurable.registry import ConfigurableRegistry
from canopsis.configuration.configurable.decorator import conf_paths
from canopsis.configuration.configurable.decorator import add_category


CONF_PATH = 'dsl/requester.conf'
CATEGORY = 'REQUESTER'
CONTENT = []


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class DSLRequester(ConfigurableRegistry):

    CONTEXT_MANAGER = 'context_manager'
    DSL_PARSER = 'dsl_parser'

    def __init__(self, context_manager=None, dsl_parser=None, *args, **kwargs):
        super(DSLRequester, self).__init__(*args, **kwargs)

        if context_manager is not None:
            self[DSLRequester.CONTEXT_MANAGER] = context_manager

        if dsl_parser is not None:
            self[DSLRequester.DSL_PARSER] = dsl_parser

    def perform(self, request):
        parsed = self[DSLRequester.DSL_PARSER].parse(request)

        sysentities = self[DSLRequester.CONTEXT_MANAGER].get(
            'system',
            parsed['systems'] + parsed['targets']
        )

        managers = [
            ConfigurableRegistry.get_configurable(entity['path'])
            for entity in sysentities
        ]
