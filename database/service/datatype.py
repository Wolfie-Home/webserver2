from .. import settings
import sqlite3
from hashlib import sha512
import random
import string
from database.service.exceptions import AlreadyExistsError, NoRecordError, UnknownError
from database.service.exceptions import assert_NoRecord


def create(name, description=''):
    """
    Create a new data type
    :param name: name of data type
    :param description: Description
    :return: sqlite3 row object. key = (`Id`,`TypeName`,`Description`)
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # Insert
            cur.execute(' \
                      INSERT INTO `DataType`(`TypeName`,`Description`) \
                        VALUES (?, ?)', (name, description))

            # Then get created object
            cur.execute(' \
                      SELECT `Id`,`TypeName`,`Description` \
                        FROM `DataType` \
                        WHERE (`TypeName` = ?)', (name,))
        except sqlite3.IntegrityError:
            con.rollback()
            raise AlreadyExistsError("Datatype name already exists.")
        except Exception as e:
            raise UnknownError(e)
        else:
            result = cur.fetchone()
        con.commit()

    return result


def get_list():
    """
    Get all list of data type
    :return: sqlite3 row object. key = (`Id`,`TypeName`,`Description`)
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # get user
            cur.execute('SELECT `Id`,`TypeName`,`Description` FROM `DataType`;')
        except Exception as e:
            raise UnknownError(e)

        result = cur.fetchall()
        assert_NoRecord(result, "No datatype record in this DB.")
    return result
