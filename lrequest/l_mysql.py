# -*- coding: UTF-8 -*-
import MySQLdb
from config import Config


class LMysql(object):
    db = None
    cursor = None
    __instance = None

    def __init__(self):
        print "LMysql init  "
        pass

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(LMysql, cls).__new__(cls)
            config = Config()
            print config.get_item("mysql", "host")
            print 'ling'
            cls.db = MySQLdb.connect(config.get_item("mysql", "host"),
                                     config.get_item("mysql", "user"),
                                     config.get_item("mysql", "password"),
                                     config.get_item("mysql", "db"),
                                     charset="utf8")
            cls.cursor = cls.db.cursor()
            print 'LMysql __new__ '
        return cls.__instance

    def count(self, sql_str):
        count = self.cursor.execute(sql_str)
        return count

    def disable_ip(self, ip):
        try:
            self.cursor.execute(
                "UPDATE pi_pool SET state = 1 WHERE ip = '{}'"
                .format(ip))
            self.db.commit()
        except Exception, e:
            print 'LMysql updatedisableip error:'
            print e
            self.db.rollback()

    def get_random_ip(self):
        data = {}
        try:
            self.cursor.execute("SELECT "
                                "* FROM pi_pool AS t1 "
                                "JOIN "
                                "( "
                                "SELECT ROUND( RAND( ) * "
                                "( "
                                "( SELECT MAX( id ) FROM pi_pool WHERE state = 0 ) - "
                                "( SELECT MIN( id ) FROM pi_pool WHERE state = 0 ) "
                                ") + "
                                "( SELECT MIN( id ) FROM pi_pool WHERE state = 0 ) ) AS id "
                                ") "
                                "AS t2 "
                                "WHERE t1.id >= t2.id "
                                "AND t1.state = 0 "
                                "ORDER BY t1.id "
                                "LIMIT 1")
            results = self.cursor.fetchall()
            for row in results:
                data['id'] = row[0]
                data['ip'] = row[1]
                data['port'] = row[2]
                data['type'] = "http" if row[3] == 1 else "https"
        except Exception, e:
            print 'LMysql getrandomip error:'
            print e
        return data

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print 'db closed !'


