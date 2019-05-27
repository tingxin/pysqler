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
        self._group_index = 0
        self._brace_added = 0

    def where(self, key, operator, value):
        part = self._g_where_value(value)
        operator = strings.get_sql_operator(operator, value)
        append = self._where.append
        if self._where:
            append("AND")
        else:
            append("WHERE")

        for i in range(0, self._group_index):
            append("(")

        self._brace_added += self._group_index
        self._group_index = 0
        append("{0} {1} {2}".format(key, operator, part))
        return self

    def and_where(self, key, operator, value):
        self.where(key, operator, value)

        return self

    def or_where(self, key, operator, value):
        part = self._g_where_value(value)
        operator = strings.get_sql_operator(operator, value)
        self._where.append("OR")

        for i in range(0, self._group_index):
            self._where.append("(")

        self._brace_added += self._group_index
        self._group_index = 0

        self._where.append("{0} {1} {2}".format(key, operator, part))
        return self

    def begin_group(self):
        self._group_index += 1

    def end_group(self):
        if self._brace_added <= 0:
            raise ValueError("Need call begin_group first")

        self._where.append(")")
        self._brace_added -= 1

    def _g_where_value(self, value):
        if not self._where:
            self._where = list()
        return strings.get_sql_str(value)
