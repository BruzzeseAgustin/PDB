import pymysql

class DBHelper:

    def __init__(self):
        self.host       = "127.0.0.1"
        self.user       = "root"
        self.port       = int(5000) 
        self.password   = "Br_4912#862"
        self.db         = "mysql"
        self.charset    = 'utf8'

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, cursorclass=pymysql.cursors.
                                   DictCursor, charset=self.charset)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()