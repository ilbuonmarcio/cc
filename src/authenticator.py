import mysql.connector
from algorithm.components.DBConfig import DBConfig
import hashlib
from random import choice
from string import hexdigits


def get_digest(password, salt):
    full_password = password + salt
    digest = hashlib.sha256(full_password.encode()).hexdigest()
    return digest


def get_hashed_password_and_salt_by_username(username):
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT hashed_password, salt FROM utenti WHERE username = '" + username + "';"
    cursor.execute(query)

    row = cursor.fetchall()[0]
    hashed_password, salt = row[0], row[1]

    cursor.close()
    connection.close()

    return hashed_password, salt


def generate_hashed_password_and_salt_by_password(password):
    random_salt = (''.join(choice(hexdigits) for _ in range(32)))
    hashed_password = get_digest(password, random_salt)

    return hashed_password, random_salt


def authenticate_user(username, password):
    hashed_password, salt = get_hashed_password_and_salt_by_username(username)
    calculated_hashed_password = get_digest(password, salt)

    return hashed_password == calculated_hashed_password


# DEBUGGING
if __name__ == "__main__":
    right_password = "123"
    wrong_password = "aaa"

    # print(generate_hashed_password_and_salt_by_password(right_password))

    print(authenticate_user('root', right_password))
    print(authenticate_user('root', wrong_password))
    # print(authenticate_user('root', wrong_password))
