import psycopg2

db_host = "image-database.cbpimzarujc3.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

# Database functions:

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

# Command line interface functions:

def print_menu():
    print("1) List Users")
    print("2) Add User")
    print("3) Edit User")
    print("4) Delete User")
    print("5) Quit")
    return input("Enter command> ")

def print_list(users):
    print("username    password    full name")
    print("---------------------------------")
    for row in users:
        print(row[0] + '    ' + row[1] + '    ' + row[2])

def main():
    connect()
    mode = "0"
    while mode != "5":
        mode = print_menu()
        if mode == "1":
            users = list_users()
            print_list(users)
        elif mode == "2":
            username = input("Username> ")
            password = input("Password> ")
            full_name = input("Full name> ")
            add_user(username,password,full_name)
        elif mode == "3":
            username = input("Username edit> ")
            if user_exists(username) == False:
                print("No such user.\n")
            else:
                password = input("New password (press enter to keep current)> ")
                full_name = input("New full name (press enter to keep current)> ")
                edit_user(username,password,full_name)
        elif mode == "4":
            username = input("Enter username to delete> ")
            verify = input("Are you sure that you want to delete " + username + "?> ")
            if verify == 'yes' or verify == 'Yes' or verify == 'Y' or verify == 'y':
                delete_user(username)
                print('deleted')
        elif mode == "5":
            break
        else:
            print("Please enter a valid number or 5 to exit.")
    print("Bye")

if __name__ == '__main__':
    main()

