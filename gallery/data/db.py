import psycopg2
import json
import os

dbname = 'image_gallery'

def get_host():
    return os.getenv("PG_HOST")

def get_port():
    return os.getenv("PG_PORT")

def get_password():
    pwfile = open(os.getenv("IG_PASSWD_FILE"), "r") 
    pw = pwfile.readline()
    pwfile.close()
    return pw[:-1]

def get_username():
    return os.getenv("IG_USER")

def get_db_name():
    return os.getenv("IG_DATABASE")

def connect():
    global connection
    connection = psycopg2.connect(host=get_host(), port=get_port(), dbname=get_db_name(), user=get_username(), password=get_password())

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)

if __name__ == '__main__':
    main()

