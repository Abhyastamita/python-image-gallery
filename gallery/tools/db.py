import psycopg2
from secrets import get_secret_image_gallery
import json

dbname = 'image_gallery'

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']

def get_db_name(secret):
    return secret['dbInstanceIdentifier']

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=dbname, user=get_username(secret), password=get_password(secret))

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

# User functions:

def list_users():
    res = execute('select * from users;')
    return res

def add_user(username,password,full_name):
    res = execute("insert into users values (%s, %s, %s);",(username,password,full_name))
    connection.commit()
    return

def user_exists(username):
    res = execute("select username from users where username = %s;",(username,))
    if res.rowcount > 0:
        return True
    else:
        return False

def edit_user(username,password=None,full_name=None):
    if password:
        res = execute("update users set password = %s where username = %s;",(password,username))
    if full_name:
        res = execute("update users set full_name = %s where username = %s;",(full_name,username))
    connection.commit()
    return

def delete_user(username):
    res = execute("delete from users where username = %s;",(username,))
    connection.commit()
    return

def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)

if __name__ == '__main__':
    main()

