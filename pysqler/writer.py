#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: barry.xu(friendship-119@163.com)
#
# Created: 2019/2/24


from .helper import Where
from .helper import strings


class Select(Where):
    """
    Build a select sql
    eg:
    >> query = Select()
    >> query.select("city", "education", "AVG(age) as avg_age")
    >> query.from1("people")
    >> query.where("age", ">", 10)
    >> query.join("orders", "orders.account = people.id",
    >>            "orders.time = people.birthday")
    >> query.and_where("job", "like", "%it%")
    >> query.and_where("birthday", ">", "1988-09-12 12:12:12")
    >> query.and_where("address", "!=", None)

    >> query.left_join("vip", "vip.account = people.id")

    >> query.groupby("city", "education")
    >> query.orderby("avg_age", "DESC")
    >> query.limit(10, 8)

    output:
    >> SELECT city,education,AVG(age) as avg_age
    >> FROM people
    >> INNER JOIN orders
    >> ON orders.account = people.id and orders.time = people.birthday
    >> LEFT JOIN vip ON vip.account = people.id
    >> WHERE age > 10 AND job like "％it％" AND birthday > "1988-09-12 12:12:12"
    >> AND address IS NOT null
    >> GROUP BY city,education ORDER BY avg_age DESC
    >> LIMIT 8,10
    """

    def __init__(self):
        super(Select, self).__init__()
        self._select = None
        self._from = None
        self._group = None
        self._order = None
        self._limit = None
        self._join = None
        self._table_index = 97

    def select(self, *fields):
        """
        :param fields: the field names in tables
        :return: self
        """
        if not self._select:
            self._select = list()

        self._select.extend(fields)
        return self

    def from1(self, table):
        """
        :param table: table name you want to select
        :return: self
        """
        if not self._from:
            self._from = list()

        self._from.append(table)
        return self

    def join_by_type(self, t, table, *conditions):
        if self._join is None:
            self._join = list()
        head = "{0} JOIN {1} ON".format(t, table)
        body = " and ".join(conditions)
        self._join.append(head)
        self._join.append(body)

    def join(self, table, *conditions):
        """
        INNER JOIN another table on conditions
        eg:
        >> query.join("orders", "orders.account = people.id",
               "orders.time = people.birthday")
        :param table: table name
        :param conditions: join conditions, eg: orders.time = people.birthday
        :return: self
        """
        self.join_by_type("INNER", table, *conditions)

    def left_join(self, table, *conditions):
        """
        LEFT JOIN another table on conditions
        eg:
        >> query.left_join("orders", "orders.account = people.id",
               "orders.time = people.birthday")
        :param table: table name
        :param conditions: join conditions, eg: orders.time = people.birthday
        :return: self
        """
        self.join_by_type("LEFT", table, *conditions)

    def right_join(self, table, *conditions):
        """
        RIGHT JOIN another table on conditions
        eg:
        >> query.right_join("orders", "orders.account = people.id",
               "orders.time = people.birthday")
        :param table: table name
        :param conditions: join conditions, eg: orders.time = people.birthday
        :return: self
        """
        self.join_by_type("RIGHT", table, *conditions)

    def full_join(self, table, *conditions):
        """
        FULL JOIN another table on conditions
        eg:
        >> query.full_join("orders", "orders.account = people.id",
               "orders.time = people.birthday")
        :param table: table name
        :param conditions: join conditions, eg: orders.time = people.birthday
        :return: self
        """
        self.join_by_type("FULL", table, *conditions)

    def groupby(self, *fields):
        """
        :param fields: the field names in tables
        :return: se
        """
        if not self._group:
            self._group = list()

        self._group.extend(fields)
        return self

    def orderby(self, field, ori="DESC"):
        """

        :param field: field order by
        :param ori: DESC or ASC, by default is DESC
        :return:
        """
        if not self._order:
            self._order = list()

        part = "{0} {1}".format(field, ori)
        self._order.append(part)
        return self

    def limit(self, count, offset=0):
        """
        :param count: the row count your query return
        :param offset: from which row you want to return
        :return: self
        """
        if offset > 0:
            self._limit = "LIMIT {0},{1}".format(offset, count)
        else:
            self._limit = "LIMIT {0}".format(count)

    def __str__(self):
        u = list()
        if self._select:
            selected = ",".join(self._select)
            u.append("SELECT")
            u.append(selected)

        if self._from:
            from_source = ",".join(self._from)
            u.append("FROM")
            u.append(from_source)

        if self._join:
            join = " ".join(self._join)
            u.append(join)

        if self._where:
            where = " ".join(self._where)
            u.append(where)

        if self._group:
            gr = ",".join(self._group)
            u.append("GROUP BY")
            u.append(gr)

        if self._order:
            gr = ",".join(self._order)
            u.append("ORDER BY")
            u.append(gr)

        if self._limit:
            u.append(self._limit)

        return " ".join(u)


class Insert:
    """
    Build a select sql
    eg:
    >> query = sqler.Insert("people")
    >> query.put("name", "jack")
    >> query.put("age", 10, value_on_duplicated=20)

    >> express = sqler.Expression()
    >> express.field("salary")
    >> express.operator("+")
    >> express.value(200)
    >> express.operator("*")
    >> express.value(3.5)

    >> query.put("salary", 5000, value_on_duplicated=express)
    >> query.put("address", "shanghai", value_on_duplicated="china")
    >> query.put("education", "bachelor")
    >> query.put("job", "engineer")
    >> query.put("birthday", "2000-01-01")
    >> query_str = str(query)
    >> print(query_str)

    output:
    >> INSERT INTO people ( name,age,salary,address,education,job,birthday )
    >> VALUES( "jack",10,5000,"shanghai","bachelor","engineer","2000-01-01" )
    >> ON DUPLICATE KEY UPDATE age = 20,salary = salary + 200 * 3.5,
    >> address = "china"

    eg2:
    >> query = sqler.Insert("people")
    >> query.add_columns("name", "age", "salary", "address",
     "education", "job", "birthday")
    >> query.add_row("barry", 19, 3100, "shanghai", "bachelor",
     None,"2010-01-01")
    >> query.add_row("jack", 24, 3600, "shanghai", "bachelor",
    "engineer","2010-01-09")
    >> query.add_row("bob", 27, 8600, None, "bachelor", "engineer","1990-01-09")
    >> query.add_row("edwin", 30, 10600, "beijing", "bachelor",
    "engineer","1987-01-09")
    >> query_str = str(query)
    >> print(query_str)

    output:
    >> INSERT INTO people ( name,age,salary,address,education,job,birthday )
    >> VALUES( "barry",19,3100,"shanghai","bachelor",null,"2010-01-01" ),
    >> ( "jack",24,3600,"shanghai","bachelor","engineer","2010-01-09" ),
    >> ( "bob",27,8600,null,"bachelor","engineer","1990-01-09" ),
    >> ( "edwin",30,10600,"beijing","bachelor","engineer","1987-01-09" )
    """

    def __init__(self, table):
        self._cache = ["INSERT INTO {0}".format(table)]
        # 0 -> init status
        # 1 -> use put
        # 2 -> use add row
        self._use_status = 0

        self._pairs = list()
        self._columns = None

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

        if not self._columns:
            msg = "should set columns first"
            raise ValueError(msg)

        if len(values) != len(self._columns):
            msg = "values count must mach columns count"
            raise ValueError(msg)

        self._use_status = 2

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
        self._cache.append("(")
        self._cache.append(",".join(self._columns))
        self._cache.append(")")
        self._cache.append("VALUES")
        values = list()
        for row in self._pairs:
            t = ",".join(row)
            p = "({0})".format(t)
            values.append(p)

        values_str = ",".join(values)
        self._cache.append(values_str)
        return " ".join(self._cache)

    def _str_simple_insert(self):
        columns = [item[0] for item in self._pairs]
        self._cache.append("(")
        self._cache.append(",".join(columns))
        self._cache.append(")")

        values = [item[1] for item in self._pairs]
        self._cache.append("VALUES(")
        t = ",".join(values)
        self._cache.append(t)
        self._cache.append(")")

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
            self._cache.append("ON DUPLICATE KEY UPDATE")
            self._cache.append(",".join(dup_pairs))

        return " ".join(self._cache)


class Update(Where):
    """
    Build update sql
    eg:
    >> query = sqler.Update("people")
    >> query.put("name", "barry")
    >> query.put("age", 10)

    >> query.where("age", ">", 15)
    >> query.or_where("age", "<", 5)
    >> query_str = str(query)
    >> print(query_str)
    output:
    >> UPDATE people SET name = "barry",age = 10
    >> WHERE age > 15 OR age < 5
    """

    def __init__(self, table):
        super(Update, self).__init__()
        self._cache = ["UPDATE {0} SET".format(table)]
        self._pairs = list()

    def put(self, key, value):
        part = strings.get_sql_str(value)
        pair = (key, part)
        self._pairs.append(pair)

        return self

    def __str__(self):
        if not self._pairs:
            return ""

        f = "{0} = {1}"
        values = [f.format(item[0], item[1]) for item in self._pairs]
        self._cache.append(",".join(values))

        if self._where:
            condition = " ".join(self._where)
            self._cache.append(condition)

        return " ".join(self._cache)


class Delete(Where):
    """
    Build delete sql
    eg:
    >> query = sqler.Delete("people")
    >> query.where("age", ">", 15)
    >> query.or_where("name", "in", [9527, "barry", "jack"])
    >> query_str = str(query)
    >> print(query_str)
    output:
    >> DELETE FROM people  WHERE age > 15 OR name in (9527,"barry","jack")
    """

    def __init__(self, table):
        super(Delete, self).__init__()
        self.table = table

    def __str__(self):
        cache = ["DELETE FROM {0} ".format(self.table)]

        if self._where:
            condition = " ".join(self._where)
            cache.append(condition)

        return " ".join(cache)


class Expression:
    def __init__(self):
        self.cache = list()

    def field(self, v):
        self.cache.append(v)

    def operator(self, v):
        self.cache.append(v)

    def value(self, v):
        v = strings.get_sql_str(v)
        self.cache.append(v)

    def __str__(self):
        return " ".join(self.cache)
