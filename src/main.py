import sqlite3

connection = sqlite3.connect('student.db')

cursor = connection.cursor()

# create db
table_info = """
create table STUDENTS(name varchar(30), class varchar(30), section varchar(3), 
marks int)"""

cursor.execute(table_info)

# insert values
cursor.execute("""insert into STUDENTS values('Yash', 'Data Science', 'A', 90),
               ('John', 'Data Science', 'B', 96),
               ('Jacob', 'Machine Learning', 'C', 88),
               ('Mark', 'Artificial Intelligence', 'A', 98);""")

print("The inserted record")

data = connection.execute("""select * from STUDENTS""")
for i in data:
    print(i)
connection.commit()
connection.close()