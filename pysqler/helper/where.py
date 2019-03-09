#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: barry.xu(friendship-119@163.com)
#
# Created: 2019/2/24

from . import strings


class Where:
    def __init__(self):
        self._where = None

    def where(self, key, operator, value):
        part = self._g_where_value(value)
        operator = strings.get_sql_operator(operator, value)
        self._where.append("WHERE {0} {1} {2}".format(key, operator, part))
        return self

    def and_where(self, key, operator, value):
        part = self._g_where_value(value)
        operator = strings.get_sql_operator(operator, value)
        self._where.append("AND {0} {1} {2}".format(key, operator, part))
        return self

    def or_where(self, key, operator, value):
        part = self._g_where_value(value)
        operator = strings.get_sql_operator(operator, value)
        self._where.append("OR {0} {1} {2}".format(key, operator, part))
        return self

    def _g_where_value(self, value):
        if not self._where:
            self._where = list()
        return strings.get_sql_str(value)
