import psycopg2
from gallery.tools.ig_secrets import get_secret_image_gallery, get_secret_host
import json

dbname = 'image_gallery'

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

# uncomment to use Ansible VPC
# def get_host():
#     return get_secret_host()

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

def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)

if __name__ == '__main__':
    main()

