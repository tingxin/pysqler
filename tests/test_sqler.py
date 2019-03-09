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
        query.limit(8, 10)

        expected = """
        SELECT city,education,AVG(age) as avg_age
        FROM people
        WHERE age > 10 AND job like "％it％"
        AND birthday > "1988-09-12 12:12:12"
        AND address IS NOT null
        GROUP BY city,education 
        ORDER BY avg_age DESC
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
        DELETE FROM people  WHERE age > 15 OR name in (9527,"barry","jack")
        """
        self.compare_sql(expected, query_str)


if __name__ == '__main__':
    unittest.main()
