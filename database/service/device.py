from .. import settings
import sqlite3
from hashlib import sha512
import random
import string
from database.service.exceptions import AlreadyExistsError, NoRecordError, UnknownError
from database.service.exceptions import assert_NoRecord


def create(name, userid, locationid=None, parentid=None, description=''):
    """
    Create a new device into db.
    :param name: Name of new device
    :param userid: owner of this device
    :param locationid: Location id where the device located
    :param parentid: mother device id
    :param description: description
    :return: sqlite3 row object. key = (`Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # Insert
            cur.execute(' \
                      INSERT INTO `Device`(`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`) \
                        VALUES (?,?,?,?,?)',
                        (userid, name, locationid, parentid, description))

            # Then get created object
            cur.execute(' \
                      SELECT `Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description` \
                        FROM `Device` \
                        WHERE (`OwnerRef` = ?) AND (`Name` = ?)', (userid, name))
        except sqlite3.IntegrityError:
            con.rollback()
            raise AlreadyExistsError("Location name already exists.")
        except Exception as e:
            raise UnknownError(e)
        else:
            result = cur.fetchone()
        con.commit()

    return result


def get(userid, idx=None, name=None, locationid=None, parentid=None):
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
                SELECT `Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description` \
                  FROM `Device` \
                  WHERE (`OwnerRef` = ?) \
                    AND ((`Id` = ?) OR (? IS NULL)) \
                    AND ((`Name` = ?) OR (? IS NULL)) \
                    AND ((`LocationRef` = ?) OR (? IS NULL)) \
                    AND ((`Parent` = ?) OR (? IS NULL))',
                        (userid, idx, idx, name, name, locationid, locationid, parentid, parentid))
        except Exception as e:
            raise UnknownError(e)

        result = cur.fetchall()
        assert_NoRecord(result, "No device record with this criteria")
    return result
