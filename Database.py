import mysql.connector # type: ignore

# Connect to the MySQL database

def Signup(username,password):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sunny@1432",
    database="Login")
    cursor = mydb.cursor()
    sql = "INSERT INTO userLogin (username, password) VALUES (%s, %s)"
    val = (username , password)  # Replace with actual values
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return 1

def Login(username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sunny@1432",
        database="Login")
    cursor = mydb.cursor()

    # Use parameters in the query to prevent SQL injection
    search_query = "SELECT * FROM userLogin WHERE username=%s AND password=%s"
    cursor.execute(search_query, (username, password))
    Log = cursor.fetchall()
    print(Log)
    if len(Log) == 0:
        return 0

    cursor.close()
    mydb.close()
    return 1
    
