from .. import settings
import sqlite3
from hashlib import sha512
import random
import string
from database.service.exceptions import AlreadyExistsError, NoRecordError, UnknownError
from database.service.exceptions import assert_NoRecord


def create(name, userid, parentid=None, description=''):
    """
    Create a new location into db.
    :param name: name of new location
    :param userid: owner of this location
    :param parentid: parent location
    :param description: extra description of location
    :return: sqlite3 row object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # Insert
            cur.execute(' \
                      INSERT INTO `Location`(`UserRef`, `Name`,`Description`,`Parent`) \
                        VALUES (?, ?, ?, ?)', (userid, name, description, parentid))

            # Then get created object
            cur.execute(' \
                      SELECT `Id`,`UserRef`,`Name`,`Description`,`Parent` \
                        FROM `Location` \
                        WHERE `UserRef` = ? AND `Name` = ?', (userid, name))
        except sqlite3.IntegrityError:
            con.rollback()
            raise AlreadyExistsError("Location name already exists.")
        except Exception as e:
            raise UnknownError(e)
        else:
            result = cur.fetchone()
        con.commit()

    return result


def get(userid, idx=None, name=None, parentid=None):
    """
    Get one location or a list of locations
    :param userid: Owner's id
    :param idx: location's id. optional
    :param parentid: Parent location id
    :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # get user
            cur.execute(' \
                SELECT `Id`,`UserRef`,`Name`,`Description`,`Parent` \
                  FROM `Location` \
                  WHERE (`UserRef` = ?) \
                    AND ((`Id` = ?) OR (? IS NULL)) \
                    AND ((`Name` = ?) OR (? IS NULL)) \
                    AND ((`Parent` = ?) OR (? IS NULL))',
                        (userid, idx, idx, name, name, parentid, parentid))
        except Exception as e:
            raise UnknownError(e)

        result = cur.fetchall()
        assert_NoRecord(result, "No location record with this criteria")
    return result
