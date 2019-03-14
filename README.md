# pysqler
Easy to write sql to avoid using string slice

更方便的拼写SQL， 免除各种容易出错的拼接字符串操作

eg:
```python
age = some_function()
sql = "select * from people where name=\'barry\' and age = {0}" 
if age:
    sql = sql.format(sql, age)
else:
    sql = sql.format(sql, "null")
    
```

above is boring, so try this:
```python
from pysqler import *

age = some_function()

query = Select()
query.select("*")
query.from1("people")
query.where("age", "=", age)
query.and_where("name", "=", "barry")
query_str = str(query)
print(query_str)
```

you don't need take care of that if if the param is string, number or none ...




## Usage
### Build Select SQL
```python
from pysqler import *
 
query = Select()
query.select("city", "education", "AVG(age) as avg_age")
query.from1("people")
query.where("age", ">", 10)
query.join("orders", "orders.account = people.id",
           "orders.time = people.birthday")
query.and_where("job", "like", "%it%")
query.and_where("birthday", ">", "1988-09-12 12:12:12")
query.and_where("address", "!=", None)

query.left_join("vip", "vip.account = people.id")

query.groupby("city", "education")
query.orderby("avg_age", "DESC")
query.limit(10, 8)

```
output
```sql
SELECT city,education,AVG(age) as avg_age
FROM people
INNER JOIN orders
ON orders.account = people.id and orders.time = people.birthday
LEFT JOIN vip ON vip.account = people.id
WHERE age > 10 AND job like "％it％" AND birthday > "1988-09-12 12:12:12"
AND address IS NOT null
GROUP BY city,education ORDER BY avg_age DESC
LIMIT 8,10;
```

### Build Insert SQl
#### insert one row
```python
from pysqler import *

query = Insert("people")
query.put("name", "barry")

query.put("age", 10, value_on_duplicated=20)

express = Expression()
express.field("salary")
express.operator("+")
express.value(200)
express.operator("*")
express.value(3.5)

query.put("salary", 1000, value_on_duplicated=express)
query.put("address", "shanghai", value_on_duplicated="china")
query.put("education", "bachelor")
query.put("job", "engineer")
query.put("birthday", "2000-01-01")
query_str = str(query)
print(query_str)
```
output:
```sql
INSERT INTO people ( name,age,salary,address,education,jobs,birthday)
VALUES("barry",10,1000,"shanghai","bachelor","engineer","2000-01-01")
ON DUPLICATE KEY UPDATE age = 20,salary = salary + 200 * 3.5,
address = "china";
```

#### insert multiple rows
```python
from pysqler import *

query = Insert("people")
query.add_columns("name", "age", "salary", "address", "education", "job", "birthday")
query.add_row("barry", 19, 3100, "shanghai", "bachelor", None,"2010-01-01")
query.add_row("jack", 24, 3600, "shanghai", "bachelor", "engineer","2010-01-09")
query.add_row("bob", 27, 8600, None, "bachelor", "engineer","1990-01-09")
query.add_row("edwin", 30, 10600, "beijing", "bachelor", "engineer","1987-01-09")
query_str = str(query)
print(query_str)

```
output:
```odpsql
INSERT INTO people ( name,age,salary,address,education,job,birthday )
 VALUES( "barry",19,3100,"shanghai","bachelor",null,"2010-01-01" ),
 ( "jack",24,3600,"shanghai","bachelor","engineer","2010-01-09" ),
 ( "bob",27,8600,null,"bachelor","engineer","1990-01-09" ),
 ( "edwin",30,10600,"beijing","bachelor","engineer","1987-01-09" )
```

### Build update SQl
```python
from pysqler import *

query = Update("people")
query.put("name", "barry")
query.put("age", 10)

query.where("age", ">", 15)
query.or_where("age", "<", 5)
query_str = str(query)
print(query_str)
```

output:
```sql
UPDATE people SET name = "barry",age = 10
WHERE age > 15 OR age < 5;
```

### Build delete SQl
```python
from pysqler import *

query = Delete("people")

query.where("age", ">", 15)
query.or_where("name", "in", [9527, "barry", "jack"])
query_str = str(query)
print(query_str)
```

output:
```sql
DELETE FROM people  WHERE age > 15 OR name in (9527,"barry","jack");
```

