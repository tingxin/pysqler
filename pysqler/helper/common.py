#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: barry.xu(friendship-119@163.com)
#
# Created: 2020/7/23


from enum import Enum, unique


@unique
class ValueType(Enum):
    Auto = 0
    Number = 1
    Bool = 2
    String = 3
    Object = 4
    List = 5
    Tuple = 6
    Date = 7
