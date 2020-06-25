import pymysql
import configparser

from sql_list import *

config = configparser.ConfigParser()

class mariaDB():
    def __init__(self):
        self.db_conn = None

    def db_connect(self):
        conn_result = False
        try:
            config.read('config.ini')
            db_ip = config['DBINFO']['IP']
            db_name = config['DBINFO']['DBNAME']
            db_port = int(config['DBINFO']['PORT'])
            db_user = config['DBINFO']['ID']
            db_pwd = config['DBINFO']['PWD']
            print(db_ip)
            print(db_name)
            print(db_port)
            print(db_user)
            print(db_pwd)
            self.db_conn = pymysql.connect(host=db_ip, port=db_port, db=db_name, user=db_user, password=db_pwd, charset='utf8')
            conn_result = True
        except Exception as e:
            print(e)

        return conn_result

    def select(self, name, group):
        temp_list = []
        try:
            sql = SELECT_QUERY
            if name is not None:
                if "WHERE" in sql:
                    sql += f"AND trvl_name LIKE '%{name}%' "
                else:
                    sql += f"WHERE trvl_name LIKE '%{name}%' "
            if group is not None:
                if "WHERE" in sql:
                    sql += f"AND trvl_group LIKE '%{group}%' "
                else:
                    sql += f"WHERE trvl_group LIKE '%{group}%' "
            print(sql)
            with self.db_conn.cursor(pymysql.cursors.DictCursor) as db_cur:
                db_cur.execute(sql)
                temp_list = db_cur.fetchall()
        except Exception as e:
            print(e)

        return temp_list

    def insert(self, name, desc, score, place, group):
        result = True
        try:
            sql = INSERT_QUERY.format(name, desc, score, place, group)
            print(sql)
            with self.db_conn.cursor() as db_cur:
                db_cur.execute(sql)
                self.db_conn.commit()
        except (pymysql.OperationalError, pymysql.InterfaceError) as e:
            result = False
            print(e)
        except Exception as e:
            result = False
            print(e)

        return result

    def update(self, seq, name, desc, score, place, group):
        result = True
        try:
            sql = UPDATE_QUERY.format(seq, name, desc, score, place, group)
            print(sql)
            with self.db_conn.cursor() as db_cur:
                db_cur.execute(sql)
                self.db_conn.commit()
        except (pymysql.OperationalError, pymysql.InterfaceError) as e:
            print(e)
        except Exception as e:
            result = False
            print(e)

        return result

    def delete(self, seq):
        result = True
        try:
            sql = DELETE_QUERY.format(seq)
            with self.db_conn.cursor() as db_cur:
                db_cur.execute(sql)
                self.db_conn.commit()
        except (pymysql.OperationalError, pymysql.InterfaceError) as e:
            print(e)
        except Exception as e:
            result = False
            print(e)

        return result






