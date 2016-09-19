from .. import settings
import sqlite3
from hashlib import sha512
import random
import string
from database.service.exceptions import AlreadyExistsError, NoRecordError, UnknownError
from database.service.exceptions import assert_NoRecord


def create(name, deviceid, datatypeid, controllable=False, description=''):
    """
    Create a new datafield of device into db.
    :param name: Name of datafield.
    :param deviceid: id of device that has the datafield
    :param datatypeid: id of datatype that the datafield uses
    :param controllable: set if this datafield is controllable or not
    :param description: description
    :return: sqlite3 row object. key = (`Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`)
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # Insert
            cur.execute(' \
                      INSERT INTO `DataField`(`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`) \
                        VALUES (?, ?, ?, ?, ?)',
                        (deviceid, name, int(controllable), datatypeid, description))

            # Then get created object
            cur.execute(' \
                      SELECT `Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description` \
                        FROM `DataField` \
                        WHERE (`DeviceRef` = ?) AND (`DatafieldName` = ?)',
                        (deviceid, name))
        except sqlite3.IntegrityError:
            con.rollback()
            raise AlreadyExistsError("Datafield name already exists for this device")
        except Exception as e:
            raise UnknownError(e)
        else:
            result = cur.fetchone()
        con.commit()

    return result


def get(deviceid):
    """
    Get all datafields of device
    :param deviceid: id of device
    :return: sqlite3 row object. key = (`Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`)
    """
    with sqlite3.connect(settings.db) as con:
        con.row_factory = sqlite3.Row  # this make cursor dictionary
        cur = con.cursor()

        try:
            # get user
            cur.execute('\
                SELECT `Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description` \
                  FROM `DataField` \
                  WHERE (`DeviceRef` = ?)',
                        (deviceid))
        except Exception as e:
            raise UnknownError(e)

        result = cur.fetchall()
        assert_NoRecord(result, "No datafield record with this criteria")
    return result
