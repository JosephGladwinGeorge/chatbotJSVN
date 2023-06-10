import mysql.connector
from mysql.connector import Error
try:
    connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='avengers007',
                    database='studentdata'
                )
    sub = 'cst201'
    user_id = '22020'
    q = f"SELECT subject_sem from semester_subject where subject_code='{sub}'"
    cursor = connection.cursor()
    cursor.execute(q)

    sem = cursor.fetchall()
    print(sem[0][0])

    query = f"SELECT series_1,series_2 FROM {sem[0][0]} where subject='{sub}' AND user_id='{user_id}'"
    cursor.execute(query)

    mark = cursor.fetchall()

    table = "| Series 1 | Series 2 |\n"
    table += "|----------|----------|\n"

    for row in mark:
        table += "|    {}    |    {}    |\n".format(row[0], row[1])
            
    print(table)
except Error as e:
            # Handle any errors that occur during the database connection or query execution
            print(f"Error connecting to MySQL: {e}")