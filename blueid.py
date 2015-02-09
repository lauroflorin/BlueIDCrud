###################################################################
# Database connection layer
###################################################################
import hashlib
import MySQLdb
import random
from random import randint
from _random import Random
import time

# Database parameters
host = "localhost"
sql_server_user = "root"
sql_server_password = "7890uiOP"
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
               #GOKU TODO this changed
               sKey = random.randrange(1000000,10000000)
               sql = "update blueid.users set stat=1,skey=%s WHERE uid='%s';" %(sKey,username)
               cursor.execute(sql)
               db.commit()
               #return "true" #this changed to:
               return sKey
            else:           
               return "false"
        except:
           print "Username not existent or data missing"
           return "false"
           
        db.close()

    def authorize(self,uid,did,gid,cha,skey):
        db = MySQLdb.connect(host,sql_server_user ,sql_server_password,database)
        cursor = db.cursor()
        print "::::::::::::::: authorizing :::::::::::::::"

        self.uid = uid;
        self.did = did;
        self.gid = gid;
        self.cha = cha;
        self.skey = skey;

        sql = "SELECT count(blueid.devices.did) FROM blueid.users INNER JOIN blueid.devices ON blueid.users.uid = blueid.devices.uid INNER JOIN blueid.devices_gates ON blueid.devices.did = blueid.devices_gates.did INNER JOIN blueid.gates ON blueid.devices_gates.gid = blueid.gates.gid WHERE blueid.users.stat = '1' AND blueid.gates.stat = '1' AND blueid.users.uid = '%s' AND blueid.users.skey = '%s' AND blueid.devices.did = '%s' AND blueid.gates.gid = '%s';" % (uid, skey, did, gid)
        ## Step 1 - are all active and can device pass through gate
        try:
            cursor.execute(sql)
            statementResults = cursor.fetchall()
            for result in statementResults:
                isAllowed = result[0]
            print isAllowed
        except:
           print "query is fucked up for whatever reason"
           isAllowed = 0

        ## Step 2 - get gate key and generate response
        print "Im in step2"
        if isAllowed == 1:
            sql ="SELECT gk FROM gates WHERE gid='%s';" % gid
            cursor.execute(sql)
            statementResults = cursor.fetchall()
            for result in statementResults:
                gkey = result[0]
            print gkey
            ServerResponse = gkey + cha + gid + did
            self.write_log(did,gid)
            return ServerResponse
        else:
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
              
    def write_log(self,did,gid):
        print "I have reached the log method"
        db = MySQLdb.connect(host,sql_server_user ,sql_server_password,database)
        cursor = db.cursor()
        act = "opened"

        print """INSERT INTO access_log (gid,timestamp_date, timestamp_time, did, act) values (%s,CURRENT_DATE ,CURRENT_TIME ,%s,%s,)""" % (gid,did,act)
        sql = """INSERT INTO access_log (gid,timestamp_date, timestamp_time, did, act) values ('%s',CURRENT_DATE ,CURRENT_TIME ,'%s','%s')""" % (gid,did,act)

        try:
              cursor.execute(sql)
              db.commit()
              print "log written"
        except Exception as e:
             print e
             db.rollback()

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
