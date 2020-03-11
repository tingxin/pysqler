from . import strings
from .expression import Expression


class InTo:
    
    def __init__(self, command, table):
        self.command = command
        self.table = table
        
        # 0 -> init status
        # 1 -> use put
        # 2 -> use add row
        self._use_status = 0
        
        self._pairs = list()
        self._columns = None
        self.last_row_item_count = None
    
    def put(self, column_name, column_value, value_on_duplicated=None):
        """
        put data when insert one row
        :param column_name: column name
        :param column_value: column value
        :param value_on_duplicated:
        :return: self
        """
        if self._use_status == 2:
            msg = "Don't use put and add_columns together in one sql"
            raise ValueError(msg)
        self._use_status = 1
        part = strings.get_sql_str(column_value)
        pair = (column_name, part, value_on_duplicated)
        self._pairs.append(pair)
        
        return self
    
    def add_columns(self, *column_names):
        """
        set columns for on insert sql, we used it to insert multiple rows
        in one sql
        :param column_names:
        :return: self
        """
        if self._use_status == 1:
            msg = "Don't use put and add_columns together in one sql"
            raise ValueError(msg)
        
        if not self._columns:
            self._use_status = 2
            self._columns = column_names
        else:
            raise ValueError("add_columns just can be used once for one insert")
    
    def add_row(self, *values):
        """
        add row data when insert multiple rows once
        :param values: column values
        :return: self
        """
        if self._use_status == 1:
            msg = "Don't use put and add_row together in one sql"
            raise ValueError(msg)
        
        if self._columns and len(values) != len(self._columns):
            msg = "values count must mach columns count"
            raise ValueError(msg)
        
        self._use_status = 2
        count = len(values)
        if self.last_row_item_count and self.last_row_item_count != count:
            msg = "values count does not mach last time"
            raise ValueError(msg)
        
        self.last_row_item_count = count
        
        parts = [strings.get_sql_str(value) for value in values]
        self._pairs.append(parts)
        
        return self
    
    def __str__(self):
        
        if self._use_status == 1:
            return self._str_simple_insert()
        
        if self._use_status == 2:
            return self._str_multiple_insert()
        
        return ""
    
    def _str_multiple_insert(self):
        cache = ["{0} INTO {1}".format(self.command, self.table)]
        if self._columns:
            cache.append("(")
            cache.append(",".join(self._columns))
            cache.append(")")
        cache.append("VALUES")
        values = list()
        for row in self._pairs:
            t = ",".join(row)
            p = "({0})".format(t)
            values.append(p)
        
        values_str = ",".join(values)
        cache.append(values_str)
        return " ".join(cache)
    
    def _str_simple_insert(self):
        cache = ["{0} INTO {1}".format(self.command, self.table)]
        columns = [item[0] for item in self._pairs]
        cache.append("(")
        cache.append(",".join(columns))
        cache.append(")")
        
        values = [item[1] for item in self._pairs]
        cache.append("VALUES(")
        t = ",".join(values)
        cache.append(t)
        cache.append(")")
        
        f = "{0} = {1}"
        dup_groups = [p for p in self._pairs if p[2]]
        dup_groups_values = list()
        for item in dup_groups:
            dup_value = item[2]
            if isinstance(dup_value, Expression):
                v = str(dup_value)
                dup_groups_values.append((item[0], v))
            elif isinstance(dup_value, str):
                part = "\"{0}\"".format(dup_value)
                dup_groups_values.append((item[0], part))
            else:
                dup_groups_values.append((item[0], dup_value))
        
        dup_pairs = [f.format(item[0], item[1]) for item in dup_groups_values]
        
        if dup_pairs:
            cache.append("ON DUPLICATE KEY UPDATE")
            cache.append(",".join(dup_pairs))
        
        return " ".join(cache)
