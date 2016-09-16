from .. import settings
import sqlite3
from hashlib import sha512
import random
import string
from database.service.exceptions import AlreadyExistsError, NoRecordError, UnknownError
from database.service.exceptions import assert_NoRecord


def create(username, password, email):
    """
    Create a new user. Password is stored salted SHA-512 hashed
    :param username: user name
    :param password: password to input
    :param email: email address
    :return: sqlite3 row object. key = ('Id', 'UserName', 'Email')
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        # create salt
        salt = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8))
        try:
            # First just put the username and email and salt
            cur.execute(' \
                      INSERT INTO `User` (`UserName`, `Password`, `Email`, `PassSalt`) \
                      VALUES (?, "", ?, ?)', (username, email, salt))
            # then get a generated idx
            cur.execute('SELECT `Id` FROM `User` WHERE `UserName` = ?', (username,))
            idx = cur.fetchone()[0]
            # put password hash
            hashed_pass = sha512((salt + password).encode()).hexdigest()
            cur.execute(' \
                      UPDATE `User` \
                        SET `Password` = ? \
                        WHERE `Id` = ?', (hashed_pass, idx))
            # Finally, login test
            cur.execute(' \
                      SELECT `Id`, `UserName`, `Email` \
                        FROM `User` \
                        WHERE (`UserName` = ?) \
                          AND (`Password` = ?)', (username, hashed_pass))
        except sqlite3.IntegrityError:
            con.rollback()
            raise AlreadyExistsError("Username already exists")
        except Exception as e:
            raise UnknownError(e)
        else:
            result = cur.fetchone()
        con.commit()

    return result


def verify(username, password):
    """
    Login user
    :param username: user name
    :param password: password input
    :return: sqlite3 row object. key = ('Id', 'UserName', 'Email')
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # get salt
            cur.execute(' \
                SELECT `Id`, `PassSalt` \
                FROM `User` \
                WHERE `UserName` = ?', (username,))
        except Exception as e:
            raise UnknownError(e)
        result = cur.fetchone()
        assert_NoRecord(result, "Username does not exist.")

        salt = result['PassSalt']

        # create salted hash
        hashed_pass = sha512((salt + password).encode()).hexdigest()

        try:
            # get user
            cur.execute(' \
                SELECT `Id`, `UserName`, `Email` \
                    FROM `User` \
                    WHERE (`UserName` = ?) \
                    AND (`Password` = ?)', (username, hashed_pass))
        except Exception as e:
            raise UnknownError(e)

        result = cur.fetchone()
        assert_NoRecord(result, "Password does not match")
    return result
