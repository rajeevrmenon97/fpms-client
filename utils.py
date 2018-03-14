#!bin/python
import pymysql.cursors
import subprocess
from subprocess import STDOUT
from pathlib import Path
import sys
import os


class fpms:

    def __init__(self):
        self.probe = ""
        self.gallery = ""
        self.score = 0
        self.connection = None

    def connectDb(self):
        try:
            self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='ssl',
                             db='db_ams',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print('Error connecting to db! \n {!r}, errno is {}'.format(e, e.args[0]))

    def getFingerprintData(self):

        self.connectDb()

        fileList = os.listdir('./fpData')
        for fileName in fileList:
            os.remove("./fpData/"+fileName)

        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT `id_no`,`fpData` FROM `registered`"
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    with open('fpData/' + row['id_no'] + '.xyt','w') as f:
                        f.write(row['fpData'].decode('unicode_escape').rstrip())

        except Exception as e:
            print('Error getting fingerprint Data! \n {!r}, errno is {}'.format(e, e.args[0]))

        finally:
            self.connection.close()

    def register(self, id_no, name, phone, email, fpTemplate):

        templatePath = Path(fpTemplate)
        if templatePath.is_file() is False:
            print("Cannot find fingerprint template!")
            return

        self.connectDb()

        with open(fpTemplate, 'rb') as f:
            blob = f.read()

        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT MAX(`serial_no`) FROM `registered`"
                cursor.execute(sql)
                result = cursor.fetchone()
                sno = result["MAX(`serial_no`)"]
                if sno is None:
                    sno = 0
                sno = sno + 1
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `registered` (`serial_no`, `name`, `id_no`, `phone_no`, `email_id`, `fpData`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (sno, name, id_no, phone, email, blob, ))
            self.connection.commit()

        except Exception as e:
            print('Error inserting into DB!\n {!r}, errno is {}'.format(e, e.args[0]))

        finally:
            self.connection.close()

    def readFingerprint(self, fileName):
        try:
            result = subprocess.check_output(['./scanner', fileName])
        except subprocess.CalledProcessError as exc:
            result = exc.output
        result = result.decode('unicode_escape').rstrip()
        print(result)
