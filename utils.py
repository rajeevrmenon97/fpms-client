#!bin/python
import pymysql.cursors
import subprocess
from subprocess import STDOUT
from pathlib import Path
import sys
import os

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class fpms:

    def __init__(self):
        self.probe = ""
        self.gallery = ""
        self.score = -1
        self.connection = None
        self.matchedID = ""

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

    def executeBinary(self, binary, arguments):
        cmd = [binary]
        cmd.extend(arguments)
        try:
            result = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as exc:
            result = exc.output
        result = result.decode('unicode_escape').rstrip()
        return result

    def readFingerprint(self, fileName):
        binary = './scanner'
        arguments = ["temp/" + fileName]
        result = self.executeBinary(binary, arguments)
        print(result)

    def compressBMP(self, fileName):
        binary = './nbis/bin/cwsq'
        arguments = ["2.25","wsq",fileName, "-raw_in", "320,480,8"]
        result = self.executeBinary(binary, arguments)
        if result is '':
            print("Compression success!")
        else:
            print("Compression error!")
            print(result)

    def minutiaeDetect(self, fileName):
        binary = './nbis/bin/mindtct'
        arguments = ["-m1",fileName, fileName[:-4]]
        result = self.executeBinary(binary, arguments)
        if result is '':
            print("Detection success!")
        else:
            print("Detection error!")
            print(result)

    def matchFingerprints(self, templateOne, templateTwo):
        self.score = 0
        binary = './nbis/bin/bozorth3'
        arguments = [templateOne, templateTwo]
        result = self.executeBinary(binary, arguments)
        if isInt(result):
            self.score = int(result)
        else:
            print(result)

    def findMatch(self, fileName):
        flag = False;
        indir = './fpData'
        for root, dirs, filenames in os.walk(indir):
            for f in filenames:
                self.matchFingerprints(fileName, 'fpData/' + f)
                if self.score > 40:
                    self.matchedID = f[:-4]
                    print(self.matchedID)
                    break


if __name__ == '__main__':
    o = fpms()
    o.getFingerprintData()
    o.readFingerprint("temp.bmp")
    o.compressBMP("temp/temp.bmp")
    o.minutiaeDetect("temp/temp.wsq")
    o.matchFingerprints("temp/temp.xyt","fpData/B150115CS.xyt")
    o.findMatch("temp/temp.xyt")
