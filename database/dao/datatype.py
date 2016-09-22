"""
dao.DataType
"""
import sqlite3


class DataType:
    def __init__(self, con):
        self.con = con
        self.con.row_factory = sqlite3.Row  # this make cursor dictionary
        self.cur = self.con.cursor()

    def insert_single(self, name, description=''):
        """
        Create a new data type
        :param name: name of data type
        :param description: Description
        :return: sqlite3 row object. key = (`name`,`description`)
        """
        self.cur.execute(' \
                      INSERT INTO `DataType`(`name`,`description`) \
                        VALUES (?, ?)',
                         (name, description))
        return

    def select_single(self, name):
        """
        get a single datatype
        :param name: name of datatype
        :return: sqlite3 row object. key = (`id`,`name`,`description`)
        """
        self.cur.execute('\
                      SELECT `id`,`name`,`description` \
                        FROM `DataType` \
                        WHERE (`name` = ?)',
                         (name,))
        result = self.cur.fetchone()
        return result

    def select_multi(self):
        """
        Get all datatypes
        :return: sqlite3 row object. key = (`id`,`name`,`description`)
        """
        self.cur.execute('SELECT `id`,`name`,`description` FROM `DataType`;')
        result = self.cur.fetchall()
        return result
    pass
