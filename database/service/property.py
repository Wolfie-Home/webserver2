from .. import settings
import sqlite3
from database.service.exceptions import AlreadyExistsError, UnknownError, NullOrEmptyInputError
from database.service.exceptions import assert_NoRecord, assert_NullOrEmptyInput
from database.dao.datarecord import DataRecord as DataRecordDao
from database.dao.datafield import DataField as DataFieldDao
from database.dao.recordfieldvalue import RecordFieldValue as RecordFieldValueDao
from database.datatype import DataType
from database.model.property import Property as PropertyModel


class Property:

    @classmethod
    def save_record_dict(cls, device_id, location_id, property_dict, time=None):
        """
                Create a new device into db.
                :param name: Name of new device
                :param userid: owner of this device
                :param location_id: Location id where the device located
                :param mother_id: mother device id
                :param description: description
                :return: sqlite3 row object. key = (`Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
                """
        assert_NullOrEmptyInput(property_dict)

        # FIXME: Time is not used????????
        # FIXME: Device name? or device ID?

        with sqlite3.connect(settings.db) as con:
            # get DAOs
            dr_dao = DataRecordDao(con)
            df_dao = DataFieldDao(con)
            rfv_dao = RecordFieldValueDao(con)

            try:
                # first insert DataRecord and git record ID
                dr_id = dr_dao.insert_single(device_id, location_id)

                # get datafield list
                result_df = df_dao.select_multi(device_id)

                # Put RecordFieldValue dictionary
                for df in result_df:
                    # match with input dict
                    key = df['name']
                    if not property_dict.get(key):
                        continue # if name is not in the input skip
                    df_id = df['id']
                    value = DataType.encode[df['type']](property_dict[key])
                    rfv_dao.insert_single(dr_id, df_id, value)
                    print(str(dr_id) + " and " + str(df_id) + " and " + str(value))
                # Then get list of datafields
                # FIXME: get result using
                # result_records = rfv_dao.select_multi()
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
        return

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
            rfv_dao = RecordFieldValueDao(con)

            try:
                # get datafield
                result_dao = df_dao.select_multi(device_id)
                # get record
                record_dict = {}
                for df in result_dao:
                    record = rfv_dao.select_multi(df['id'])
                    if record:
                        copy = dict(record[len(record) - 1])
                        copy['value'] = DataType.decode[df['type']](copy['value'])
                        record_dict[df['name']] = copy
                    else:
                        record_dict[df['name']] = None
                pass
            except Exception as e:
                con.rollback()
                raise UnknownError(e)

            assert_NoRecord(result_dao, "No device record with this criteria")
            result = []
            for df in result_dao:
                prop = PropertyModel(**df)
                prop.records.append(record_dict[df['name']])
                result.append(prop)
        return result
    pass
