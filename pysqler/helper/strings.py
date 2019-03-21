#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: barry.xu(friendship-119@163.com)
#
# Created: 2019/2/24


import re


def replace(str_content, rep):
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    my_str = pattern.sub(lambda m: rep[re.escape(m.group(0))], str_content)
    return my_str


def filter_sql(sql):
    if sql == "":
        return sql

    rep = dict()
    rep["'"] = "‘"
    rep[";"] = "；"
    rep[","] = "，"
    rep["?"] = "？"
    rep["<"] = "＜"
    rep[">"] = "＞"
    rep["("] = "（"
    rep[")"] = "）"
    rep["="] = "＝"
    rep["+"] = "＋"
    rep["*"] = "＊"
    rep["&"] = "＆"
    rep["#"] = "＃"
    rep["$"] = "￥"

    sql = replace(sql, rep)
    return sql


def get_sql_str(v):
    if v is None:
        part = "null"
    elif isinstance(v, str):
        part = filter_sql(v)
        part = "\"{0}\"".format(part)
    elif isinstance(v, tuple):
        return handel_tuple(v)
    elif isinstance(v, list):
        t = tuple(v)
        return handel_tuple(t)
    else:
        part = str(v)
    return part


def get_sql_operator(operator, v):
    if v is None:
        if operator == "=":
            return "IS"
        elif operator == "!=":
            return "IS NOT"
    return operator


def handel_tuple(v):
    if len(v) == 1:
        item = v[0]
        if isinstance(item, str):
            part = filter_sql(item)
            part = "\'{0}\'".format(part)
        else:
            part = str(item)
        return "({0})".format(part)
    else:
        return str(v)
