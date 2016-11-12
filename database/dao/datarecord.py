"""
dao.DataField
"""
import sqlite3


class DataRecord:
    def __init__(self, con):
        self.con = con
        self.con.row_factory = sqlite3.Row  # this make cursor dictionary
        self.cur = self.con.cursor()

    def insert_single(self, device_id, location_id):
        """
        Create a new data record into db.
        :param device_id: id of device that has the data record
        :param location_id: id of location where the device located
        :return: id of the new record
        """
        self.cur.execute(' \
                  INSERT INTO `DataRecord`(`device_id`,`location_id`) \
                    VALUES (?, ?)',
                         (device_id, location_id))
        return self.cur.lastrowid   # return id of record
    pass
