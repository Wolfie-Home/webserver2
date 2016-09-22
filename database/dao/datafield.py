"""
dao.DataField
"""
import sqlite3


class DataField:
    def __init__(self, con):
        self.con = con
        self.con.row_factory = sqlite3.Row  # this make cursor dictionary
        self.cur = self.con.cursor()

    def insert_single(self, name, device_id, type_id, controllable=False, description=''):
        """
        Create a new datafield of device into db.
        :param name: Name of datafield.
        :param device_id: id of device that has the datafield
        :param type_id: id of datatype that the datafield uses
        :param controllable: set if this datafield is controllable or not
        :param description: description
        :return: sqlite3 row object. key = (`Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`)
        """
        self.cur.execute(' \
                  INSERT INTO `DataField`(`device_id`,`name`,`controllable`,`type_id`,`description`) \
                    VALUES (?, ?, ?, ?, ?)',
                         (device_id, name, int(controllable), type_id, description))
        return

    def select_multi(self, device_id):
        """
        Get all datafields of device
        :param device_id: id of device
        :return: sqlite3 row object. key = (`Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`)
        """
        self.cur.execute('\
            SELECT `DataField`.`id`, \
                    `device_id`, \
                    `DataField`.`name`, \
                    `controllable`, \
                    `DataType`.`name` AS `type`, \
                    `DataField`.`description` \
              FROM `DataField` \
              JOIN `DataType`\
              ON `DataField`.`type_id` = `DataType`.`id`\
              WHERE (`device_id` = ?)',
                         (device_id,))
        result = self.cur.fetchall()
        return result
    pass
