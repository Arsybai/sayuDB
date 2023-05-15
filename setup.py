import setuptools

setuptools.setup(
    name="sayuDB",
    version="1.0.0",
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
    entry_points={
        "console_scripts": [
            "sayuDB = sayuDB.__main__:main",
            "sayudb = sayuDB.__main__:main"
        ]
    },
    long_description_content_type="text/markdown",
    long_description="""![banner](https://images.arsybai.app/images/pOMsOCbxLR.png)
---
# Preface
### What is sayuDB
sayuDB is an database management system based on python and JSON. Developed at Clee Ltd. This project actually for personal purpose only but for some reason I publish it.
It supports a large part of the SQL standard feature

# Tutorial
##### Table of contents

- [Installation](#installation)
- [Create or remove user](#Create_or_remove_user)
- [Grant privileges to user](#Grant_privileges_to_user)
- [Create and drop database](#Create_and_drop_database)
- [Import and export database](#Import_and_export_database)
- [Activate or deactivate server](#Activate_or_deactivate_server)
- [Using the sayuDB](#Using_the_sayuDB)
- [Create table](#Create_table)
- [Drop table](#Drop_table)
- [Show table](#Show_table)
- [Insert](#Insert)
- [Select](#Select)
- [Where](#Where)
- [Update](#Update)
- [Delete](#Delete)
- [Alter table](#Alter_table)
- [Clear table](#Clear_table)
---

### Installation
```shell
> pip3 install sayuDB
```
and if you want to show help menu just 
```
> python3 -m sayuDB --h
```

### Create or remove user
To create a user you can command by
```shell
> python3 -m sayuDB create user <username> <password>
```
and if you want to remove user you can command by
```shell
> python3 -m sayuDB remove user <username>
```
Note that creating or removing user only can be user when you have root/local access.
the user is use for remote database. if you want to user this database locally, you didn't need this.

And for show user, you can command by
```shell
> python3 -m sayuDB show users
```

### Grant privileges to user
Ofcourse you need to grant user to some database first before use it remotely.
Grant it by command
```shell
> python3 -m sayuDB grant user <username> <database_name>
```
### Create and drop database
To create a database, just command by
```shell
> python3 create database <database_name>
```
And to drop/delete it, just command by
```shell
> python3 -m sayuDB drop database <database_name>
```
Anyway, you can also show databases by
```shell
> python3 -m sayuDB show databases
```
### Import and export database
To import a database, just command by
```shell
> python3 -m sayuDB import database <path_to_ezdb_file>
```
And for export it, just command by
```shell
> python3 -m sayuDB export database <database_name> <output_path>
```
### Activate or deactivate server
If you want the database remotely online. just activate server by
```shell
> python3 -m sayuDB activate server <port>
```
_`Note: I recomended use 8787 as port`_
then acces it within your server IP.
if you didn't see something, try make the server public by
```shell
> python3 -m sayuDB setup public server <server_name> <port>
```
The `server_name` is your server IP or a domain that already set A record to your server IP.
And the `port` must be same when you activate it.

If you want to deactivate it, just command by
```shell
> python3 -m sayuDB deactivate server
```
---
### Using the sayuDB
To user sayu db in python, just define it first by
```python
import sayuDB # Importing the sayuDB
db = sayuDB.sayuDB("testdb") # call the class
```
The parameters are
|parameter|status|description|
|-|-|-|
`database`|required|the database name
`username`|optional|the username for you sayuDB account if you access it remotely
`password`|optional|ofc the password
`host`|optional|the host of your database hosted in
`as_json`|optional|this is the boolean if you want to return the database as json or just printed table.
### Create table
To create a table use this following function
```python
db.create_table("<table_name>", col=[
    ["number","int"],
    ["name","str"],
    ["age","int"],
    ["address","str"]
])
```
The parameters are
|parameter|status|description|
|-|-|-|
`name`|required|the name of table you want to create
`col`|required|a lists that contain list wich contain the column name and datatypes `[ ["<column_name>","<datatypes>"] ]`

> Note: supported datatypes `str`,`float`,`int`,`dict`

### Drop table
You can drop table by use this dollowing function
```python
db.drop_table("<table_name>")
```
The parameters are
|parameter|status|description|
|-|-|-|
`name`|required|the name of the table you want to drop/delete

### Show table
you can show the table by use this following funtion.
```python
db.show_table("<table_name>")
```
it will returned
```shell
number    name    age    address
--------  ------  -----  ---------
```
### Insert
To insert some row to the table, you can use this following function
```python
db.insert_row(table="<table_name>", col="number,name,age,address", contents=[1,"Arsybai",23,"Solo, Indonesia"])
```
The parameters are
|parameter|status|description|
|-|-|-|
`table`|required|The name of table you want to insert a row
`col`|required|the column that you want to insert. separate by comma or you can use list
`contents`|required|the contents/value for each column

and now if you show the table it will look like this
```shell
  number  name       age  address
--------  -------  -----  ---------------
       1  Arsybai     23  Solo, Indonesia
```

and you can also insert it with some function. as example I want to insert moepoi as number 2. but I want the number automatically increased.
```python
db.insert_row(table="<table_name>", col="number,name,age,address", contents=["increase()","Moepoi",20,"Jakarta, Indonesia"])
```
So, I use '`increase()' function for it. then the table will look like this
```shell
  number  name       age  address
--------  -------  -----  ------------------
       1  Arsybai     23  Solo, Indonesia
       2  Moepoi      20  Jakarta, Indonesia
```
Table of functions
|name|description|
|-|-|
`today()`|Generate today datetime (only work in str typedata)
`index()`|Indexing the number of row. it can be use as id too (only work in int typedata)
`genID()`|Generate random 5 digits ID
`increase()`|Increase from the last row value (Only work in int typedata)

### Select
To select a table, use this following function
```python
db.select_row(table="<table_name>", col="name,age")
```
|parameter|status|description|
|-|-|-|
`table`:`str`|required|the name of table that you want to select
`col`:`str`|required|the column name that you want to select. it separated by comma. or you can use `col="*"` if you want to select all comuns
`where`:`str`|optional|select the specific row.
`as_json`:`bool`|optional|if you already define it in the `sayuDB` class, you didn't need to do it again. the default is `False`

### Where
Now, if you want to select specific row, you can use `where` parameter for it
##### Equal or not equal.
as example, I want to select `Arsybai` from table.
```python
db.select_row(table="<table_name>", col="*", where="name=Arsybai")
```
Otherwise, if you want to select row that isn't `Arsybai` use `where="name!=Arsybai"`
The return will look like this
```shell
  number  name       age  address
--------  -------  -----  ---------------
       1  Arsybai     23  Solo, Indonesia

1 Rows
```
##### contains
If you want to select row that contain someting. you can use ` contain `.
as example I want to select name that contain `poi`
```python
db.select_row(table="<table_name>", col="*", where="name contain poi")
```
The return will look like this
```shell
  number  name      age  address
--------  ------  -----  ------------------
       2  Moepoi     20  Jakarta, Indonesia

1 Rows
```
##### Using multiple condition
as example I want to select `Arsybai` with age `20`
```python
db.select_row(table="<table_name>", col="*", where="name=Arsybai && age=20")
```
The return will look like this
```shell
number    name    age    address
--------  ------  -----  ---------

0 Rows
```
> Note : You can use `AND ( && )`, `OR ( || )` in multiple condition. also the space between && or || is required

### Update
If you want to update a row, use this following function
```python
db.update_row(table="<table_name>", set_="<column_name>=<value>", where="<column_name>=<value>")
```
Note that update row isn't support multiple condition.

Also you can update a row more efficienly with `update_row_json`
```python
db.update_row_json(table="<table_name>", set_={"<col1_name>":"<value1>","<col2_name>":"<value2>"}, where="<col_name>=<value>")
```

### Delete
If you want to delete some row, use this following function
```python
#to delete specific data that equal with some value
db.delete_row(table="<table_name>", where="<col_name>=<value>")

#to delete specific data that contain some value
db.delete_row(table="<table_name>", where="<col_name> contain <value>")

#to delete specific data with row number
db.delete_row(table="<table_name>", where="row <number_of_row>")

#to delete specific data between row number
db.delete_row(table="<table_name>", where="row between <number_of_rowX>-<number_of_rowY>")
```
### Alter table
To alter or updating some table, use this following function
```python
# to add a column
db.alter_table_add_column(table="<table_name>", col_name="<col_name>", datatypes="<datatype>")

# to remove a column
db.alter_table_drop_column(table="<table_name>", col_name="<col_name>")

# to rename a column
db.alter_table_rename_column(table="<table_name>", col="<column_to_rename>", to_="<rename_to>")
```
### Clear table
To clear table use this following function
```python
db.clear_table(table="<table_name>")
```
This will erase all rows data in the table.
"""
)