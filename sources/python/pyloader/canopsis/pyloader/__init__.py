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

__version__ = '0.1'

from canopsis.middleware.registry import MiddlewareRegistry
from canopsis.configuration.configurable.decorator import conf_paths
from canopsis.configuration.configurable.decorator import add_category

from six import PY2
import sys
import imp


CONF_PATH = 'python/loader.conf'
LOADER_CATEGORY = 'LOADER'
FINDER_CATEGORY = 'FINDER'


@conf_paths(CONF_PATH)
@add_category(LOADER_CATEGORY)
class StorageLoader(MiddlewareRegistry):

    CODE_STORAGE = 'code_storage'

    def __init__(self, code_storage=None, *args, **kwargs):
        super(StorageLoader, self).__init__(*args, **kwargs)

        if code_storage is not None:
            self[StorageLoader.CODE_STORAGE] = code_storage

    def load_module(self, fullname):
        modname = fullname[len(__name__) + 1:]

        self.logger.debug('load_module(modname={0})'.format(modname))
        doc = self[StorageLoader.CODE_STORAGE].get_elements(ids=modname)
        module = imp.new_module(fullname)

        if PY2:
            exec doc['src'] in module.__dict__

        else:
            exec(doc['src'], module.__dict__)

        sys.modules[fullname] = module
        return module


@conf_paths(CONF_PATH)
@add_category(FINDER_CATEGORY)
class StorageFinder(MiddlewareRegistry):

    CODE_STORAGE = 'code_storage'

    def __init__(self, code_storage=None, *args, **kwargs):
        super(StorageFinder, self).__init__(*args, **kwargs)

        if code_storage is not None:
            self[StorageFinder.CODE_STORAGE] = code_storage

    def find_module(self, module_name, package_name):
        if module_name.startswith(__name__):
            modname = module_name[len(__name__) + 1:]

            self.logger.debug(
                'find_module(module_name={0}, package_name={1}'.format(
                    modname,
                    package_name
                )
            )

            result = self[StorageFinder.CODE_STORAGE].get_elements(ids=modname)

            if result is not None:
                return StorageLoader()


sys.meta_path.append(StorageFinder())
