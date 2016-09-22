"""

"""

import sqlite3


class Location:
    def __init__(self, con):
        self.con = con
        self.con.row_factory = sqlite3.Row  # this make cursor dictionary
        self.cur = self.con.cursor()

    def insert_single(self, name, user_id, house_id=None, description=''):
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
                          INSERT INTO `Location`(`user_id`, `name`,`description`,`house_id`) \
                            VALUES (?, ?, ?, ?)', (user_id, name, description, house_id))
        return

    def select_single(self, user_id, id=None, name=None):
        """
        Get one location or a list of locations
        :param user_id: Owner's id
        :param id: location's id. optional
        :param house_id: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        self.cur.execute(' \
            SELECT `id`, \
                    `user_id`, \
                    `name`, \
                    `description`, \
                    `house_id`, \
                    (SELECT `name` FROM `Location` AS `B` WHERE (`B`.`id` = `A`.`house_id`)) AS `house` \
                    FROM `Location` AS `A` \
                    WHERE `user_id` = ? \
                      AND ((`id` = ?) OR (? IS NULL)) \
                      AND ((`name` = ?) OR (? IS NULL))',
                            (user_id, id, id, name, name))
        result = self.cur.fetchone()
        return result

    def select_multi(self, user_id, id=None, name=None, house_id=None):
        """
        Get one location or a list of locations
        :param user_id: Owner's id
        :param id: location's id. optional
        :param house_id: Parent location id
        :return: sqlite3 row list object. key = (`Id`,`UserRef`,`Name`,`Description`,`Parent`)
        """
        self.cur.execute(' \
                    SELECT `id`,`user_id`,`name`,`description`,`house_id` \
                      FROM `Location` \
                      WHERE (`user_id` = ?) \
                        AND ((`id` = ?) OR (? IS NULL)) \
                        AND ((`name` = ?) OR (? IS NULL)) \
                        AND ((`house_id` = ?) OR (? IS NULL))',
                            (user_id, id, id, name, name, house_id, house_id))
        result = self.cur.fetchall()
        return result
