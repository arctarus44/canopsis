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

from canopsis.configuration.configurable import Configurable
from canopsis.configuration.configurable.decorator import conf_paths
from canopsis.configuration.configurable.decorator import add_category

import sqlparse


CONF_PATH = 'dsl/parser.conf'
CATEGORY = 'PARSER'
CONTENT = []


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class DSLParser(Configurable):
    def __init__(self, *args, **kwargs):
        super(DSLParser, self).__init__(*args, **kwargs)

    def find_tokens_by_class(self, tokens, classes):
        return [
            tok
            for tok in tokens
            if isinstance(tok, classes)
        ]

    def find_matching_tokens(self, tokens, ttype, values=None):
        return [
            tok
            for tok in tokens
            if tok.match(ttype, values)
        ]

    def get_token_idx(self, tokens, ttype, values=None):
        toks = self.find_matching_tokens(tokens, ttype, values)

        if len(toks) > 0:
            tok = toks[0]

            for i in range(len(tokens)):
                if tok is tokens[i]:
                    return i

        return -1

    def parse_targets(self, tokens):
        fromidx = self.get_token_idx(tokens, sqlparse.tokens.Keyword, 'from')
        toks = []

        if fromidx >= 0:
            matching = lambda tok: any([
                tok.match(sqlparse.tokens.Name, None),
                tok.natch(sqlparse.tokens.Punctuation, None)
            ])

            i = fromidx + 1

            while matching(tokens[i]):
                if tokens[i].match(sqlparse.tokens.Name, None):
                    toks.append(tokens[i])

                i += 1

        return toks

    def parse_systems(self, tokens):
        return set([
            tokens[i]
            for i in range(len(tokens))
            if tokens[i].match(sqlparse.tokens.Name, None)
            and tokens[i + 1].match(sqlparse.tokens.Punctuation, None)
        ])

    def parse_conditions(self, tokens):
        pass

    def parse_statement(self, statement):
        tokens = [
            tok
            for tok in statement.flatten()
            if not tok.is_whitespace()
        ]

        dmltoks = [
            tok.value
            for tok in self.find_matching_tokens(
                tokens,
                sqlparse.tokens.Keyword.DML
            )
        ]

        return {
            'type': dmltoks[0],
            'targets': [tok.value for tok in self.parse_targets(tokens)],
            'systems': [tok.value for tok in self.parse_systems(tokens)]
        }

    def parse_request(self, request):
        parsed = sqlparse.parse(request)
        return map(self.parse_statement, parsed)
