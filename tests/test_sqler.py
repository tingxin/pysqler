import unittest

from pysqler import *


class SearchTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def compare_sql(self, expected, actually):
        v1 = expected.replace("\n", "")
        v1 = v1.replace(" ", "")

        v1 = v1.lower()

        v2 = actually.replace("\n", "")
        v2 = v2.replace(" ", "")
        v2 = v2.lower()

        self.assertEqual(v1, v2, "sqler.Select() build  sql error")

    def test_sql_select(self):
        query = Select()
        query.select("city", "education", "AVG(age) as avg_age")
        query.from1("people")
        query.where("age", ">", 10)
        query.and_where("job", "like", "%it%")
        query.and_where("birthday", ">", "1988-09-12 12:12:12")
        query.and_where("address", "!=", None)
        query.groupby("city", "education")
        query.orderby("avg_age", "DESC")
        query.limit(10, 8)

        expected = """
        SELECT city,education,AVG(age) as avg_age
        FROM people
        WHERE age > 10 AND job like "%%it%%"
        AND birthday > "1988-09-12 12:12:12"
        AND address IS NOT null
        GROUP BY city,education 
        ORDER BY avg_age DESC
        LIMIT 8,10
        """

        query_str = str(query)
        print(query_str)
        self.compare_sql(expected, query_str)

        q2 = Select()
        q2.select("city", "education", "AVG(age) as avg_age"). \
            from1("people"). \
            where("age", ">", 10).and_where("job", "like", "%it%"). \
            and_where("birthday", ">", "1988-09-12 12:12:12"). \
            and_where("address", "!=", None). \
            groupby("city", "education").orderby("avg_age", "DESC").limit(10, 8)
        self.compare_sql(expected, str(q2))

    def test_sql_select2(self):
        def get_sql(*params):
            query = Select()
            query.select("max(id) as last_id")
            query.from1("udp.{0}".format("table"))
            query.where("resource_type", "in", params)
            sql = str(query)
            return sql

        query_str = get_sql("content")
        print(query_str)

        expected = """
        SELECT max(id) as last_id FROM udp.table WHERE resource_type in
        ('content')
        """

        self.compare_sql(expected, query_str)

    def test_sql_select3(self):
        query = Select()
        df = "DATE_FORMAT({0}.{1},'{2}') as dt"
        create_time = df.format("c", "create_time", "%Y-%m")
        query.choice(create_time)
        query.choice("c.visibility as vi")
        query.choice("SUM(c.image_count) as sum_images")
        query.from1("comment as c")

        query.begin_group()

        query.begin_group()
        query.where("c.id", ">", 441690)
        query.or_where("c.id", "<", 241690)
        query.end_group()

        query.begin_group()
        query.where("c.like_count", ">", 100)
        query.or_where("c.like_count", "<", 10)
        query.end_group()

        query.end_group()

        query.or_where("c.visibility", "in", ['banned', 'invisible'])

        query.groupby("dt", "vi")
        query.having("sum_images", ">", 100)
        query.orderby("c.id")

        expected = """
        select DATE_FORMAT(c.create_time, '%Y-%m') as dt, c.visibility as vi, 
        SUM(c.image_count) as sum_images 
        from   comment as c 
        where ((c.id > 441690 or c.id < 241690) 
        and (c.like_count > 100 
        or c.like_count < 10)) 
        or c.visibility in ('banned','invisible')  
        group by dt, vi
        having sum_images > 100
        order by c.id desc
        """

        query_str = str(query)
        print(query_str)
        self.compare_sql(expected, query_str)

    def test_sql_join(self):
        query = Select()
        query.select("city", "education", "AVG(age) as avg_age")
        query.from1("people")
        query.where("age", ">", 10)
        query.join("orders", "orders.account = people.id",
                   "orders.time = people.birthday")
        query.and_where("job", "like", "%it%")
        query.and_where("birthday", ">", "1988-09-12 12:12:12")
        query.and_where("address", "!=", None)
        query.and_where("is_employee", "=", True)

        query.left_join("vip", "vip.account = people.id")

        query.groupby("city", "education")
        query.orderby("avg_age", "DESC")
        query.limit(10, 8)

        expected = """
        SELECT city,education,AVG(age) as avg_age
        FROM people
        INNER JOIN orders
        ON orders.account = people.id and orders.time = people.birthday
        LEFT JOIN vip ON vip.account = people.id
        WHERE age > 10 AND job like "%%it%%" AND birthday > "1988-09-12 12:12:12"
        AND address IS NOT null AND is_employee = True
        GROUP BY city,education ORDER BY avg_age DESC
        LIMIT 8,10
        """

        query_str = str(query)
        print(query_str)
        self.compare_sql(expected, query_str)

    def test_sql_insert1(self):
        query = Insert("people")
        query.put("name", "barry")

        query.put("age", 10, value_on_duplicated=20)

        express = Expression()
        express.field("salary")
        express.operator("+")
        express.value(200)
        express.operator("*")
        express.value(3.5)

        query.put("salary", 50000, value_on_duplicated=express)
        query.put("address", "shanghai", value_on_duplicated="china")
        query.put("education", "bachelor")
        query.put("job", None)
        query.put("birthday", "2000-01-01")
        query_str = str(query)
        print(query_str)

        expected = """
        INSERT INTO people ( name,age,salary,address,education,job,birthday )
        VALUES( "barry",10,50000,"shanghai","bachelor",null,"2000-01-01" )
        ON DUPLICATE KEY UPDATE age = 20,salary = salary + 200 * 3.5,
        address = "china"
        """
        self.compare_sql(expected, query_str)

    def test_sql_insert2(self):
        query = Insert("people")
        query.add_columns("name", "age", "salary", "address", "education",
                          "job", "birthday")

        query.add_row("barry", 19, 3100, "shanghai", "bachelor", None,
                      "2010-01-01")

        query.add_row("jack", 24, 3600, "shanghai", "bachelor", "engineer",
                      "2010-01-09")

        query.add_row("bob", 27, 8600, None, "bachelor", "engineer",
                      "1990-01-09")

        query.add_row("edwin", 30, 10600, "beijing", "bachelor", "engineer",
                      "1987-01-09")

        query_str = str(query)
        print(query_str)

        expected = """
        INSERT INTO people ( name,age,salary,address,education,job,birthday )
        VALUES( "barry",19,3100,"shanghai","bachelor",null,"2010-01-01" ),
        ( "jack",24,3600,"shanghai","bachelor","engineer","2010-01-09" ),
        ( "bob",27,8600,null,"bachelor","engineer","1990-01-09" ),
        ( "edwin",30,10600,"beijing","bachelor","engineer","1987-01-09" )
        
        """
        self.compare_sql(expected, query_str)

    def test_sql_insert3(self):
        from datetime import date
        query = Insert("people")
        day = date(2010, 1, 1)

        query.add_row("barry", 19, 3100, "shanghai", "bachelor", None,
                      day)

        query.add_row("jack", 24, 3600, "shanghai", "bachelor", "engineer",
                      "2010-01-09")

        query.add_row("bob", 27, 8600, None, "bachelor", "engineer",
                      "1990-01-09")

        query.add_row("edwin", 30, 10600, "beijing", "bachelor", "engineer",
                      "1987-01-09")

        query_str = str(query)
        print(query_str)

        expected = """
           INSERT INTO people
           VALUES( "barry",19,3100,"shanghai","bachelor",null,"2010-01-01" ),
           ( "jack",24,3600,"shanghai","bachelor","engineer","2010-01-09" ),
           ( "bob",27,8600,null,"bachelor","engineer","1990-01-09" ),
           ( "edwin",30,10600,"beijing","bachelor","engineer","1987-01-09" )

           """
        self.compare_sql(expected, query_str)

    def test_sql_replace(self):
        query = Replace("people")

        query.add_row("barry", 19, 3100, "shanghai", "bachelor", None,
                      "2010-01-01")

        query.add_row("jack", 24, 3600, "shanghai", "bachelor", "engineer",
                      "2010-01-09")

        query.add_row("bob", 27, 8600, None, "bachelor", "engineer",
                      "1990-01-09")

        query.add_row("edwin", 30, 10600, "beijing", "bachelor", "engineer",
                      "1987-01-09")

        query_str = str(query)
        print(query_str)

        expected = """
           REPLACE INTO people
           VALUES( "barry",19,3100,"shanghai","bachelor",null,"2010-01-01" ),
           ( "jack",24,3600,"shanghai","bachelor","engineer","2010-01-09" ),
           ( "bob",27,8600,null,"bachelor","engineer","1990-01-09" ),
           ( "edwin",30,10600,"beijing","bachelor","engineer","1987-01-09" )

           """
        self.compare_sql(expected, query_str)

    def test_sql_update1(self):
        query = Update("people")
        query.put("name", "barry")
        query.put("age", 10)

        query.where("age", ">", 15)
        query.or_where("age", "<", 5)
        query_str = str(query)
        print(query_str)

        expected = """
        UPDATE people SET name = "barry",age = 10
        WHERE age > 15 OR age < 5
        """
        self.compare_sql(expected, query_str)

    def test_sql_delete1(self):
        query = Delete("people")

        query.where("age", ">", 15)
        query.or_where("name", "in", [9527, "barry", "jack"])
        query_str = str(query)
        print(query_str)

        expected = """
        DELETE FROM people  WHERE age > 15 OR name in (9527,'barry','jack')
        """
        self.compare_sql(expected, query_str)


if __name__ == '__main__':
    unittest.main()
