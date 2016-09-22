from .. import settings
import sqlite3
from database.service.exceptions import AlreadyExistsError, UnknownError
from database.dao.datatype import DataType as DataTypeDao


class DataType:
    @classmethod
    def create(cls, name, description=''):
        """
        Create a new data type
        :param name: name of data type
        :param description: Description
        :return: sqlite3 row object. key = (`Id`,`TypeName`,`Description`)
        """
        with sqlite3.connect(settings.db) as con:
            # get Dao
            dao = DataTypeDao(con)

            try:
                # Insert
                dao.insert_single(name, description)

                # Then get created object
                result = dao.select_single(name)
            except sqlite3.IntegrityError:
                con.rollback()
                raise AlreadyExistsError("Datatype name already exists.")
            except Exception as e:
                con.rollback()
                raise UnknownError(e)
            con.commit()

        return result

    @classmethod
    def get_list(cls):
        """
        Get all list of data type
        :return: sqlite3 row object. key = (`Id`,`TypeName`,`Description`)
        """
        with sqlite3.connect(settings.db) as con:
            # get Dao
            dao = DataTypeDao(con)

            try:
                # get user
                result = dao.select_multi()
            except Exception as e:
                raise UnknownError(e)

        return result
