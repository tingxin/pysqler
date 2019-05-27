#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: barry.xu(friendship-119@163.com)
#
# Created: 2019/5/27


from . import strings


class Filter:
    def __init__(self, key):
        self.key = key
        self._conditions = None
        self._group_index = 0
        self._brace_added = 0

    def add(self, key, operator, value):
        part = self._g_value(value)
        operator = strings.get_sql_operator(operator, value)
        append = self._conditions.append
        if self._conditions:
            append("AND")
        else:
            append(self.key)

        for i in range(0, self._group_index):
            append("(")

        self._brace_added += self._group_index
        self._group_index = 0
        append("{0} {1} {2}".format(key, operator, part))
        return self

    def add_or(self, key, operator, value):
        part = self._g_value(value)
        operator = strings.get_sql_operator(operator, value)
        self._conditions.append("OR")

        for i in range(0, self._group_index):
            self._conditions.append("(")

        self._brace_added += self._group_index
        self._group_index = 0

        self._conditions.append("{0} {1} {2}".format(key, operator, part))
        return self

    def begin_group(self):
        self._group_index += 1

    def end_group(self):
        if self._brace_added <= 0:
            raise ValueError("Need call begin_group first")

        self._conditions.append(")")
        self._brace_added -= 1

    def _g_value(self, value):
        if not self._conditions:
            self._conditions = list()
        return strings.get_sql_str(value)

    def __str__(self):
        if self._conditions:
            result = " ".join(self._conditions)
            return result
        return ""
