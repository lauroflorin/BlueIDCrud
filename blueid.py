###################################################################
# Database connection layer
###################################################################
import hashlib
import MySQLdb
from random import randint

# Database parameters
host = "localhost"
sql_server_user = "root"
sql_server_password = ""
database = "blueid"

class crud:


    def login(self,username,password):
        db = MySQLdb.connect(host,sql_server_user ,sql_server_password,database)
        cursor = db.cursor()
        print "::::::::::::::: db connected :::::::::::::::"

        # sql = """CREATE TABLE IF NOT EXISTS users(uid VARCHAR(40) PRIMARY KEY,pw VARCHAR(255) NOT NULL,stat BOOLEAN NOT NULL DEFAULT FALSE);INSERT INTO users (uid,pw,stat) VALUES (admin,%s,1) ;""" %

        self.username = username;
        self.password = password;
        sql = "SELECT * FROM blueid.users WHERE uid='%s';" % username

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                uid = row[0]
                pwd = row[1]
                stat = row[2]

           # hashy = uid + pwd + str(randint(0, 999))
            #print "this is the session key: " + hashlib.sha224(hashy).hexdigest()
            if pwd == self.password:
               # return hashlib.sha224(hashy).hexdigest()
               sql = "update blueid.users set stat=1 WHERE uid='%s';" % username
               cursor.execute(sql)
               db.commit()
               return "true"
            else:           
               return "false"
        except:
           print "Username not existent or data missing"
           return "false"
           
        db.close()
              
    def logout(self,username):
        db = MySQLdb.connect(host,sql_server_user ,sql_server_password,database)
        cursor = db.cursor()
        print "::::::::::::::: db connected :::::::::::::::"

        # sql = """CREATE TABLE IF NOT EXISTS users(uid VARCHAR(40) PRIMARY KEY,pw VARCHAR(255) NOT NULL,stat BOOLEAN NOT NULL DEFAULT FALSE);INSERT INTO users (uid,pw,stat) VALUES (admin,%s,1) ;""" %

        self.username = username;
        sql = "update blueid.users set stat=0 WHERE uid='%s';" % username

        try:
            cursor.execute(sql)
            db.commit()
            return "true"
        except:
           print"Username not existent or data missing"
           db.rollback()           
           return "false"
        db.close()
              
              

    def initial_setup(self):
        db = MySQLdb.connect(host,sql_server_user ,sql_server_password,database)
        cursor = db.cursor()
        print "::::::::::::::: db setup :::::::::::::::"

        sql = """CREATE TABLE IF NOT EXISTS blueid.users(uid VARCHAR(40) PRIMARY KEY,pw VARCHAR(255) NOT NULL,stat BOOLEAN NOT NULL DEFAULT FALSE)"""
        try:
              cursor.execute(sql)
              db.commit()
              print "initial setup made1"
        except Exception as e:
             print "failed to execute1"  + e
             db.rollback()
        
        sql = """SELECT * FROM blueid.users WHERE uid='admin'"""
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            isAdmin = "true"
        except:
            isAdmin = "false"
        
        if isAdmin == "false":
            sql = """INSERT INTO blueid.users(uid,pw,stat) VALUES ('admin','password',1);"""

            try:
                cursor.execute(sql)
                db.commit()
                print "initial setup made2"
            except Exception as e:
                print "failed to execute2 " + e.message
                db.rollback()
                
        cursor.close()
        db.close()