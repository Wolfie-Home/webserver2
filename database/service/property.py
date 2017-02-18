from .. import settings
import sqlite3
from database.service.exceptions import AlreadyExistsError, UnknownError, NullOrEmptyInputError
from database.service.exceptions import assert_NoRecord, assert_NullOrEmptyInput
from database.dao.datafield import DataField as DataFieldDao
from database.model.property import Property as PropertyModel


class Property:
    @classmethod
    def get_list(cls, user_id, device_id):
        """
        Get one location or a list of locations
        :param userid: Owner's id
        :param idx: location's id. optional
        :param parentid: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        # FIXME: The user_id parameter MUST used for query, for security
        # FIXME: "Controllable" returns 1 or 0, not True/False
        with sqlite3.connect(settings.db) as con:
            # get DAOs
            df_dao = DataFieldDao(con)

            try:
                # get user
                result_dao = df_dao.select_multi(device_id)
                pass
            except Exception as e:
                con.rollback()
                raise UnknownError(e)

            assert_NoRecord(result_dao, "No device record with this criteria")
            result = []
            for df in result_dao:
                result.append(PropertyModel(**df))
        return result
    pass
