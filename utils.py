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

def getNumberOfLines(fileName):
    with open(fileName) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

class fpms:

    def __init__(self):
        self.probe = ""
        self.gallery = ""
        self.score = -1
        self.connection = None
        self.matchedID = ""
        self.templateLineCount = 0

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
            exit()

        finally:
            self.connection.close()

    def register(self, id_no, name, phone, email, fpTemplate):

        templatePath = Path(fpTemplate)
        if templatePath.is_file() is False:
            print("Cannot find fingerprint template!")
            exit()

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
            exit()

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

    def scanFingerprint(self, fileName):
        binary = './scanner'
        arguments = ["temp/" + fileName]
        result = self.executeBinary(binary, arguments)
        if result is not '':
            print(result)

    def compressBMP(self, fileName):
        binary = './nbis/bin/cwsq'
        arguments = ["2.25","wsq",fileName, "-raw_in", "320,480,8"]
        result = self.executeBinary(binary, arguments)
        if result is not '':
            print("Compression error!")
            print(result)
            exit()

    def minutiaeDetect(self, fileName):
        binary = './nbis/bin/mindtct'
        arguments = ["-m1",fileName, fileName[:-4]]
        result = self.executeBinary(binary, arguments)
        if result is not '':
            print("Detection error!")
            print(result)
            exit()

    def matchFingerprints(self, templateOne, templateTwo):
        self.score = 0
        binary = './nbis/bin/bozorth3'
        arguments = [templateOne, templateTwo]
        result = self.executeBinary(binary, arguments)
        if isInt(result):
            self.score = int(result)
        else:
            print(result)
            exit()

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

    def readFingerprint(self):
        self.scanFingerprint("temp.bmp")
        self.compressBMP("temp/temp.bmp")
        self.minutiaeDetect("temp/temp.wsq")
        self.templateLineCount = getNumberOfLines("temp/temp.xyt")

    def markAttendance(self):
        while o.templateLineCount < 35:
            o.readFingerprint()
        o.findMatch('temp/temp.xyt')
        self.connectDb()
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `attendance` (`userid`) VALUES (%s)"
                cursor.execute(sql, (self.matchedID, ))
            self.connection.commit()

        except Exception as e:
            print('Error inserting into DB!\n {!r}, errno is {}'.format(e, e.args[0]))
            exit()

        finally:
            self.connection.close()



if __name__ == '__main__':
    o = fpms()
    o.getFingerprintData()
    o.markAttendance()
