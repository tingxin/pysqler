#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: barry.xu(friendship-119@163.com)
#
# Created: 2019/2/24

from . import ValueType
from . import filter


class Where(filter.Filter):
    def __init__(self):
        super(Where, self).__init__("WHERE")
    
    def where(self, key, operator, value, value_type=ValueType.Auto):
        self.add(key, operator, value, value_type)
        return self
    
    def and_where(self, key, operator, value, value_type=ValueType.Auto):
        self.add(key, operator, value, value_type)
        return self
    
    def or_where(self, key, operator, value, value_type=ValueType.Auto):
        self.add_or(key, operator, value, value_type)
        return self
