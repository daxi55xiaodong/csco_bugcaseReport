'''http://www.cnblogs.com/hongten/p/hongten_python_sqlite3.html'''
import sqlite3
import os,sys

reload(sys)
sys.setdefaultencoding('utf-8')

class ManageDB(object):
#    DB_FILE_PATH = ''
#    TABLE_NAME = ''
    def __init__(self, path, showlog):
        self.path = path
        self.SHOW_LOG = showlog
    def get_db_conn(self):
        if os.path.exists(self.path) and os.path.isfile(self.path):
            conn = sqlite3.connect(self.path)
            return conn
    def get_db_cursor(self, conn):
        if conn is not None:
            return conn.cursor()
    def close_db(self, conn):
        try:
            if conn is not None:
                conn.close()
        finally:
            if conn is not None:
                conn.close()

    def table_drop(self, conn, table):
        if table is not None and table != '':
            sql = 'DROP TABLE IF EXISTS ' + table
            if self.SHOW_LOG:
                print '>>>>Fun:table_drop Start: excute SQL:[{}]'.format(sql)
            conn = self.get_db_conn()
            cu = self.get_db_cursor(conn)
            cu.execute(sql)
            conn.commit()
            if self.SHOW_LOG:
                print '>>>>Fun:table_drop End: excute SQL:[{}] done'.format(sql)
            self.close_db(conn)
        else:
            if self.SHOW_LOG:
                print '>>>>Fun:table_drop the [{}] seems empty'.format(table)
    def table_create(self, conn, sql):
        if sql is not None and sql != '':
            cu = self.get_db_cursor(conn)
            if self.SHOW_LOG:
                print '>>>>Fun:table_create Start: excuet SQL:[{}]'.format(sql)
            cu.execute(sql)
            conn.commit()
            if self.SHOW_LOG:
                print '>>>>Fun:table_create End: excuet SQL:[{}] done'.format(sql)
            self.close_db(conn)
        else:
            if self.SHOW_LOG:
                print '>>>>Fun:table_create [{}] seems empty'.format(sql)
    def data_save(self, conn, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_db_cursor(conn)
                for d in data:
                    if self.SHOW_LOG:
                        print '>>>>Fun:data_save Start: excute SQL: [{}], Parameter: [{}]'.format(sql, d)
                    cu.execute(sql, d)
                    conn.commit()
                self.close_db(conn)
        else:
            if self.SHOW_LOG:
                print '>>>>Fun:data_save [{}] seems empty'.format(sql)
    def data_fetchall(self, conn, sql):
        if sql is not None and sql != '':
            cu = self.get_db_cursor(conn)
            if self.SHOW_LOG:
                print '>>>>Fun:data_fetchall Start: excuet SQL:[{}]'.format(sql)
            cu.execute(sql)
            res = cu.fetchall()
            if len(res) > 0:
                return res
            else:
                return "NONE_DATA"
        else:
            if self.SHOW_LOG:
                print '>>>>Fun:data_fetchall [{}] seems empty'.format(sql)

    def data_fetchone(self, conn, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                d = (data, )
                cu = self.get_db_cursor(conn)
                if self.SHOW_LOG:
                    print '>>>>Fun:data_fetchone Start: excute SQL: [{}], Parameter: [{}]'.format(sql, data)
                cu.execute(sql, d)
                res = cu.fetchall()
                if len(res) > 0:
                    return res
                else:
                    return "NONE_DATA"
            else:
                if self.SHOW_LOG:
                    print 'Fun:data_fetchone >>>>[{}] seems NONE'.format(data)
        else:
            if self.SHOW_LOG:
                print '>>>>Fun:data_fetchone [{}] seems empty'.format(sql)
    def data_update(self, conn, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_db_cursor(conn)
                for d in data:
                    if self.SHOW_LOG:
                        print '>>>>Fun:data_update Start: excute SQL: [{}], Parameter: [{}]'.format(sql, d)
                    cu.execute(sql, d)
                    conn.commit()
            self.close_db(conn)
        else:
            if self.SHOW_LOG:
                print '>>>>Fun:data_update [{}] seems empty'.format(sql)
    def data_delete(self, conn, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_db_cursor(conn)
                for d in data:
                    if self.SHOW_LOG:
                        print '>>>>Fun:data_delete Start: excute SQL: [{}], Parameter: [{}]'.format(sql, d)
                    cu.execute(sql, d)
                    conn.commit()
                self.close_db(conn)
        else:
            if self.SHOW_LOG:
                print '>>>>Fun:data_delete [{}] seems empty'.format(sql)
