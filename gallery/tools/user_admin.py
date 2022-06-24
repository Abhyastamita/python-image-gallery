import psycopg2
from gallery.tools.db import *




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

