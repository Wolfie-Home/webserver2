from .. import settings
import sqlite3
from database.datatype import DataType
from database.service.exceptions import AlreadyExistsError, UnknownError, NullOrEmptyInputError
from database.service.exceptions import assert_NoRecord, assert_NullOrEmptyInput
from database.dao.device import Device as DeviceDao
from database.dao.datafield import DataField as DataFieldDao
from database.model.device import Device as DeviceModel
from database.model.property import Property


class Device:

    @classmethod
    def create(cls, name, userid, datafield_list, location_id=None, mother_id=None, description=''):
        """
        Create a new device into db.
        :param name: Name of new device
        :param userid: owner of this device
        :param location_id: Location id where the device located
        :param mother_id: mother device id
        :param description: description
        :return: sqlite3 row object. key = (`Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
        """
        assert_NullOrEmptyInput(datafield_list)

        with sqlite3.connect(settings.db) as con:
            # get DAOs
            dev_dao = DeviceDao(con)
            df_dao = DataFieldDao(con)

            try:
                # Insert
                dev_dao.insert_single(name, userid, location_id, mother_id, description)

                # Then get created object
                result_dev = dev_dao.select_single(userid, name=name)

                # Put datafields here
                for obj in datafield_list:
                    df = {}
                    df["name"] = obj["name"]
                    df["device_id"] = result_dev["id"]
                    df["type_id"] = DataType.datatypes[obj["type"]].id
                    df["controllable"] = obj["controllable"]
                    df["description"] = obj["description"]
                    df_dao.insert_single(**df)
                    pass

                # Then get list of datafields
                result_dfs = df_dao.select_multi(result_dev["id"])

            except sqlite3.IntegrityError:
                con.rollback()
                raise AlreadyExistsError("Location name already exists.")
            except KeyError as e:
                con.rollback()
                raise NullOrEmptyInputError("Datafield list format is incorrect.")
            except Exception as e:
                con.rollback()
                raise UnknownError(e)
            else:
                con.commit()

        device = DeviceModel(**result_dev)
        for df in result_dfs:
            device.properties.append(Property(**df))
        return device

    @classmethod
    def get(cls, user_id, id=None, name=None):
        """
        Get one location or a list of locations
        :param userid: Owner's id
        :param idx: location's id. optional
        :param parentid: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """

        with sqlite3.connect(settings.db) as con:
            # get DAOs
            dev_dao = DeviceDao(con)

            try:
                # get user
                result_dao = dev_dao.select_single(user_id, id, name)
                pass
            except Exception as e:
                con.rollback()
                raise UnknownError(e)

            assert_NoRecord(result_dao, "No device record with this criteria")
            result = DeviceModel(**result_dao)
        return result

    @classmethod
    def get_list(cls, user_id, location_id=None, mother_id=None):
        """
        Get one location or a list of locations
        :param userid: Owner's id
        :param idx: location's id. optional
        :param parentid: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """

        with sqlite3.connect(settings.db) as con:
            # get DAOs
            dev_dao = DeviceDao(con)

            try:
                # get user
                result_dao = dev_dao.select_multi(user_id, location_id, mother_id)
                pass
            except Exception as e:
                con.rollback()
                raise UnknownError(e)

            assert_NoRecord(result_dao, "No device record with this criteria")
            result = []
            for obj in result_dao:
                result.append(DeviceModel(**obj))
        return result
    pass
