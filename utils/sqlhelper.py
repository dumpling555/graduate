import pymysql

def getall(sql,args):#获取列表
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getone(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result



def modify(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    conn.commit()
    cursor.close()
    conn.close()


class SqlHelper(object):
    def __init__(self):

        self.connect()#初始化就连接
    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dangdang')
        self.cursor =self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def getall(self,sql,args):
        self.cursor.execute(sql,args)
        result=self.cursor.fetchall()
        return result
    def getone(self,sql,args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result
    def modify(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multiple_modify(self,sql,args):
        self.cursor.executemany(sql,args)

    def create(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.lastrowid#row id是自增的，可以拿来直接用，当做老师的id

    def close(self):
        self.cursor.close()
        self.conn.close()





