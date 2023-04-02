import setuptools

setuptools.setup(
    name="sayuDB",
    version="0.0.5",
    author="Arsybai",
    description="Database management system based on python and JSON.",
    packages=["sayuDB"],
    license="MIT",
    author_email="me@arsybai.com",
    url="https://github.com/Arsybai/sayuDB",
    keywords=[
        'database',
    ],
    install_requires=[
    'requests',
    'tabulate',
    'flask'
    ],
    long_description_content_type="text/markdown",
    long_description="""# Documentation

##### Table of content
###### Preface
1. [What is sayuDB](#1_What_is_sayuDB_18)

###### Tutorial
1. [Getting Started](#1-getting-started)
- 1.1 [Installation](#11-installation)
- 1.2 [Creating database](#12-creating-database)
- 1.3 [Creating a New Table](#13-creating-a-new-table)
- 1.4 [Populating a table with rows](#14-pupulating-a-table-with-rows)
- 1.5 [Querying a Table](#15-querying-a-table)
- 1.6 [Updates](#updates)
- 1.7 [Deletion](#17-deletion)

---
# Preface
### 1. What is sayuDB
sayuDB is an database management system based on python and JSON. Developed at Clee Ltd. This project actually for personal purpose only but for some reason I publish it.
It supports a large part of the SQL standard feature

# Tutorial
### 1. Getting Started
#### 1.1 Installation
Before you can use sayuDB you need to install it, of course.
Just clone this repository and place it to your project folder.
```shell
> pip3 install sayuDB
```
for help menu:
```shell
> python3 sayuDB --h
```

#### 1.2 Creating database
The first test to see whether you can access the database server is to try to create a database.

To create a new database, in this example named `myDB`, you use the following funtion:
```python
import sayuDB

# Creating database
sayuDB.create_database('myDB')
```
You can also create databases with other names. sayuDB allows you to create any number of databases at a given site. Database names must have an alphabetic first character, can not contain space and are limited to 63 bytes in length.

If you do not want to use your database anymore you can remove it. For example, you can destroy it using the following function:
```python
import sayuDB

sayuDB.drop_database('myDB')
```

You can import export using:
```python
# Exporting database (must use file name)
sayuDB.export_database('<name_of_database>', path_='<path>/filename.ezdb')
# Importing database
sayuDB.import_database(path_='/<path>/filename.ezdb')
```

#### 1.3 Creating a New Table
You can create a new table by specifying the table name, along with all column names and their types:

you must define the database first with:
```python
import sayuDB

db = sayuDB.sayuDB(database='myDB')
```

then
```python
db.create_table('people', [
    ['name','str'],
    ['age','int'],
    ['city','str']
])
```
sayuDB currenly support data types `str`,`int`,`float`,`dict`

If you want to show the table, using this following function:
```python
db.show_table(name='people')
```
it will returned as printed table:
```shell
name    column    datas
------  --------  -------
```

Finally, it should be mentioned that if you don't need a table any longer or want to recreate it differently you can remove it using the following function:
```python
db.drop_table(name='people')
```

#### 1.4 Populating a Table With Rows
The `insert_row` function is used to populate a table with rows:
```python
db.insert_row(table='people', col='name,age,city', contents=['Arsybai', 23, 'Solo, Indonesia'])
```
_You can also use col as list. EX `['name','age','city']`_

### 1.5 Querying a Table
To retrieve data from a table, the table is queried. An `select_row` funtion is used to do this. The funtion is divided into a select list (the part that lists the columns to be returned), a table list (the part that lists the tables from which to retrieve the data), and an optional qualification (the part that specifies any restrictions). For example, to retrieve all the rows of table `people`, type:
```python
data = db.select_row(table='people', col='*')
print(data)
```
Here `*` is a shorthand for “all columns”. So the same result would be had with:
```python
db.select_row(table='people', col='name,age,city')
```
The output should be:
```shell
name       age  city
-------  -----  ------------------
Arsybai     23  Solo, Indonesia
Ataro       25  Bekasi, Indonesia
Moepoi      21  Jakarta, Indonesia
```

If you want the output is json, use `as_json=True`:
```python
data = db.select_row(table='people', col='*', as_json=True)
print(data)
```

A query can be “qualified” by adding a `where` clause that specifies which rows are wanted:
```python
data = db.select_row(table='people', col='*', where='age=23')
print(data)
```
you can also use ` contain ` for specific column that contain some value:
```python
data = db.select_row(table='people', col='*', where='age contain 23')
print(data)
```
Result:
```shell
name       age  city
-------  -----  ---------------
Arsybai     23  Solo, Indonesia
```

You can request that the results of a query be returned in sorted order:
```python
data = db.select_row(table='people', col='*', order_by='age|asc')
print(data)
```
_The order should be `asc` or `desc`_

Result:
```shell
name       age  city
-------  -----  ------------------
Moepoi      21  Jakarta, Indonesia
Arsybai     23  Solo, Indonesia
Ataro       25  Bekasi, Indonesia
```

#### Updates
You can update existing rows using the `update_row`.
as example I want to set `Ataro` age to `26`:
```python
db.update_row(table='people', set_='age=26', where='name=Ataro')
```
Look at the new state of the data:
```shell
name       age  city
-------  -----  ------------------
Arsybai     23  Solo, Indonesia
Ataro       26  Bekasi, Indonesia
Moepoi      21  Jakarta, Indonesia
```

#### Deletion
Rows can be removed from a table using the `delete_row`:
```python
db.delete_row(table='people', where='name=Ataro')
```

Look at the new state of the data:
```shell
name       age  city
-------  -----  ------------------
Arsybai     23  Solo, Indonesia
Moepoi      21  Jakarta, Indonesia
```
"""
)