from .. import settings
import sqlite3
from hashlib import sha512
import random
import string


def create(username, password, email):
    """
    Create a new user. Password is stored salted SHA-512 hashed
    :param username: user name
    :param password: password to input
    :param email: email address
    :return: sqlite3 row object. key = ('Id', 'UserName', 'Email')
    """
    con = sqlite3.connect(settings.db)
    con.row_factory = sqlite3.Row  # this make cursor dictionary
    cur = con.cursor()

    # create salt
    salt = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8))

    # First just put the username and email and salt
    cur.execute(' \
            INSERT INTO `User` (`UserName`, `Password`, `Email`, `PassSalt`) \
            VALUES (?, "", ?, ?)', (username, email, salt))

    # then get a generated id
    cur.execute('SELECT `Id` FROM `User` WHERE `UserName` = ?', (username,))
    id = cur.fetchone()[0]

    # put password hash
    hashed_pass = sha512((salt + password).encode()).hexdigest()
    cur.execute(' \
            UPDATE `User` \
              SET `Password` = ? \
              WHERE `Id` = ?', (hashed_pass, id))

    # Finally, login test
    cur.execute(' \
            SELECT `Id`, `UserName`, `Email` \
              FROM `User` \
              WHERE (`UserName` = ?) \
                AND (`Password` = ?)', (username, hashed_pass))
    result = cur.fetchone()

    con.commit()
    return result


def login(username, password):
    """
    Login user
    :param username: user name
    :param password: password input
    :return: sqlite3 row object. key = ('Id', 'UserName', 'Email')
    """
    con = sqlite3.connect(settings.db)
    con.row_factory = sqlite3.Row  # this make cursor dictionary
    cur = con.cursor()

    # get salt
    cur.execute(' \
        SELECT `Id`, `PassSalt` \
        FROM `User` \
        WHERE `UserName` = ?', (username,))
    result = cur.fetchone()
    id = result['Id']
    salt = result['PassSalt']

    # create hash
    hashed_pass = sha512((salt + password).encode()).hexdigest()

    # get user
    cur.execute(' \
        SELECT `Id`, `UserName`, `Email` \
            FROM `User` \
            WHERE (`UserName` = ?) \
            AND (`Password` = ?)', (username, hashed_pass))
    result = cur.fetchone()

    con.commit()
    return result
