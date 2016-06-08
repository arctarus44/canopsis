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

from b3j0f.conf import Configurable, category
from link.dbrequest.driver import Driver

from link.mongo.ast.insert import ASTInsertTransform
from link.mongo.ast.filter import ASTFilterTransform

from canopsis.middleware.core import Middleware as CanopsisMiddleware


@Configurable(
    paths='storage/dbrequest/driver.conf'.format(CONF_BASE_PATH),
    conf=category('CANOPSIS')
)
class CanopsisDriver(Driver):

    __protocols__ = ['canopsis']

    def _connect(self):
        protocol, data_type, data_scope = self.path
        middleware = CanopsisMiddleware.get_middleware(
            protocol,
            data_type,
            data_scope
        )
        middleware.connect()

        return middleware

    def _disconnect(self, conn):
        conn.disconnect()

    def _isconnected(self, conn):
        return conn is not None and conn.connected()

    def _process_query(self, conn, query):
        if query['type'] == Driver.QUERY_COUNT:
            ast = query['filter']
            mfilter = self.ast_to_filter(ast)

            _, count = self.conn.find_elements(
                query=mfilter
            )

            return count

        if query['type'] == Driver.QUERY_CREATE:
            ast = query['update']
            doc = self.ast_to_insert(ast)

            result = self.conn.put_element(doc)

            return result

        elif query['type'] == Driver.QUERY_READ:
            ast = query['filter']
            mfilter, s = self.ast_to_filter(ast)

            cursor = self.conn.find_elements(
                query=mfilter,
                skip=s.start or 0,
                limit=s.stop or 0
            )

            return cursor

        elif query['type'] == Driver.QUERY_UPDATE:
            filter_ast, _ = query['filter']
            update_ast = query['update']

            mfilter = self.ast_to_filter(filter_ast)
            uspec = self.ast_to_update(update_ast)

            return self.conn._update(
                mfilter,
                uspec
            )

        elif query['type'] == Driver.QUERY_DELETE:
            ast = query['filter']
            mfilter, _ = self.ast_to_filter(ast)

            return self.conn.remove_elements(_filter=mfilter)

    def ast_to_insert(self, ast):
        transform = ASTInsertTransform(ast)
        return transform()

    def ast_to_filter(self, ast):
        transform = ASTFilterTransform(ast)
        return transform()

    def ast_to_update(self, ast):
        doc = self.ast_to_insert(ast)

        update_set = {
            key: value
            for key, value in doc.items()
            if value is not None
        }

        update_unset = {
            key: value
            for key, value in doc.items()
            if value is None
        }

        return {
            '$set': update_set,
            '$unset': update_unset
        }
