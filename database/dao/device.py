"""
dao.Device
"""

import sqlite3


class Device:
    def __init__(self, con):
        self.con = con
        self.con.row_factory = sqlite3.Row  # this make cursor dictionary
        self.cur = self.con.cursor()

    def insert_single(self, name, user_id, location_id=None, mother_id=None, description=''):
        """
        Create a new device into db.
        :param cur: db cursor
        :param name: Name of new device
        :param user_id: owner of this device
        :param location_id: Location id where the device located
        :param mother_id: mother device id
        :param description: description
        :return: sqlite3 row object. key = (`Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
        """
        self.cur.execute(' \
            INSERT INTO `Device`(`user_id`,`name`,`location_id`,`mother_id`,`description`) \
              VALUES (?,?,?,?,?)', (user_id, name, location_id, mother_id, description))
        return

    def select_single(self, user_id, id=None, name=None):
        """
        Get one location or a list of locations
        :param user_id: Owner's id
        :param id: location's id. optional
        :param mother_id: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        self.cur.execute(' \
            SELECT `Device`.`id`, \
                  `Device`.`user_id`, \
                  `Device`.`name`, \
                  `location_id`, \
                  `Location`.`name` AS `location`, \
                  `mother_id`, \
                  `Device`.`description` \
              FROM `Device` \
              JOIN `Location` \
              ON (`Location`.`id` = `Device`.`mother_id`) OR (`Device`.`mother_id` IS NULL) \
              WHERE (`Device`.`user_id` = ?) \
                AND ((`Device`.`id` = ?) OR (? IS NULL)) \
                AND ((`Device`.`name` = ?) OR (? IS NULL))',
                         (user_id, id, id, name, name))
        result = self.cur.fetchone()
        return result

    def select_multi(self, user_id, location_id=None, mother_id=None):
        """
        Get one location or a list of locations
        :param user_id: Owner's id
        :param id: location's id. optional
        :param mother_id: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        self.cur.execute(' \
            SELECT `id`,`user_id`,`name`,`location_id`,`mother_id`,`description` \
              FROM `Device` \
              WHERE (`user_id` = ?) \
                AND ((`location_id` = ?) OR (? IS NULL)) \
                AND ((`mother_id` = ?) OR (? IS NULL))',
                         (user_id, location_id, location_id, mother_id, mother_id))
        result = self.cur.fetchall()
        return result
