"""
dao.DataField
"""
import sqlite3


class RecordFieldValue:
    def __init__(self, con):
        self.con = con
        self.con.row_factory = sqlite3.Row  # this make cursor dictionary
        self.cur = self.con.cursor()

    def insert_single(self, record_id, datafield_id, value):
        """
        Create a new datafield of device into db.
        :param record_id: ID of record.
        :param datafield_id: id of datafield.
        :param value: value in string
        :return: nothing
        """
        self.cur.execute(' \
                  INSERT INTO `RecordFieldValue`(`value`,`record_id`,`datafield_id`) \
                    VALUES (?, ?, ?)',
                         (value, record_id, datafield_id))
        return

    def select_multi(self, datafield_id, device_id=None, location_id=None):
        """
        Get all record values of device
        :param datafield_id: datafield_id of record
        :param device_id: id of device
        :param location_id: location id of device
        :return: sqlite3 row object. key = (`value`,`time`)
        """
        # TODO: Do we need device_id???
        self.cur.execute('\
            SELECT A.`value` AS `value`, \
                    B.`created_time` AS `time`\
              FROM `RecordFieldValue` AS A\
              JOIN (SELECT `id`, `created_time`\
                    FROM `DataRecord`\
                    WHERE ((`device_id` = ?) OR (? IS NULL))\
                      AND ((`location_id` = ?) OR (? IS NULL))\
                    ) AS B\
              ON B.`id` = A.`record_id`\
              WHERE (A.`datafield_id` = ?)',
                         (device_id, device_id, location_id, location_id, datafield_id))
        result = self.cur.fetchall()
        return result
    pass
