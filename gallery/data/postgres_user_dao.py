from . import db
from .user import User
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass
    
    def list_users(self):
        result = []
        cursor = db.execute('select username, password, full_name from users;')
        for row in cursor.fetchall():
            result.append(User(row[0], row[1], row[2]))
        return result

    def user_exists(self, username):
        res = db.execute("select username from users where username = %s;",(username,))
        if res.rowcount > 0:
            return True
        else:
            return False

    def add_user(self, username,password,full_name):
        if self.user_exists(username):
            return False
        res = db.execute("insert into users values (%s, %s, %s);",(username,password,full_name))
        db.connection.commit()
        return True

    def get_user(self, username):
        cursor = db.execute("select username, password, full_name from users where username = %s;",(username,))
        row = cursor.fetchone()
        if row == None:
            return None
        else:
            return User(row[0], row[1], row[2])

    def edit_user(self, username,password=None,full_name=None):
        if not self.user_exists(username):
            return False
        if password:
            res = db.execute("update users set password = %s where username = %s;",(password,username))
        if full_name:
            res = db.execute("update users set full_name = %s where username = %s;",(full_name,username))
        db.connection.commit()
        return True

    def delete_user(self, username):
        res = db.execute("delete from users where username = %s;",(username,))
        db.connection.commit()
        return