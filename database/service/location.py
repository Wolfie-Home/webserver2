from .. import settings
import sqlite3
from database.service.exceptions import AlreadyExistsError, UnknownError
from database.service.exceptions import assert_NoRecord
from database.model.location import Location as LocationModel
from database.dao.location import Location as LocationDao


class Location:
    @classmethod
    def create(cls, name, user_id, house_id=None, description=''):
        """
        Create a new location into db.
        :param name: name of new location
        :param user_id: owner of this location
        :param house_id: parent location
        :param description: extra description of location
        :return: sqlite3 row object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        with sqlite3.connect(settings.db) as con:
            # get DAO
            dao = LocationDao(con)

            try:
                # Insert
                dao.insert_single(name, user_id, house_id, description)

                # Then get created object
                result = dao.select_single(user_id, name=name)
            except sqlite3.IntegrityError:
                con.rollback()
                raise AlreadyExistsError("Location name already exists.")
            except Exception as e:
                con.rollback()
                raise UnknownError(e)
            else:
                con.commit()

            result = LocationModel(**result)
        return result

    @classmethod
    def get(cls, user_id, id=None, name=None):
        """
        Get one location or a list of locations
        :param user_id: Owner's id
        :param id: location's id. optional
        :param house_id: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        with sqlite3.connect(settings.db) as con:
            # get DAO
            dao = LocationDao(con)

            try:
                # get object
                result_mother = dao.select_single(user_id, id=id, name=name)
            except Exception as e:
                raise UnknownError(e)

            result = LocationModel(**result_mother)
        return result

    @classmethod
    def get_list(cls, user_id, id=None, name=None, house_id=None):
        """
        Get one location or a list of locations
        :param user_id: Owner's id
        :param id: location's id. optional
        :param house_id: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        with sqlite3.connect(settings.db) as con:
            # get DAO
            dao = LocationDao(con)

            try:
                # get location list
                result_dao = dao.select_multi(user_id, id, name, house_id)
            except Exception as e:
                raise UnknownError(e)

            assert_NoRecord(result_dao, "No location record with this criteria")

            result = []
            for obj in result_dao:
                result.append(LocationModel(**obj))
        return result
