#!bin/python
import pymysql.cursors
import subprocess
from subprocess import STDOUT
from pathlib import Path
import sys
import os
import re

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

def cleanTemp():
    dir_name = "temp"
    dirs = os.listdir(dir_name)
    for item in dirs:
        if item.endswith(".bmp") or item.endswith(".brw") or item.endswith(".dm") or item.endswith(".hcm") or item.endswith(".lcm") or item.endswith(".lfm") or item.endswith(".min") or item.endswith(".qm") or item.endswith(".wsq"):
                os.remove(os.path.join(dir_name, item))

class fpms:

    def __init__(self):
        self.probe = ""
        self.gallery = ""
        self.score = -1
        self.connection = None
        self.matchedID = ""
        self.matchedName = ""
        self.templateLineCount = 0

    def connectDb(self):
        try:
            self.connection = pymysql.connect(host='192.168.3.111',
                             user='amsuser',
                             password='amspassword',
                             db='db_ams',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print('Error connecting to db! \n {!r}, errno is {}'.format(e, e.args[0]))
            return -1

    def getFingerprintData(self):

        if self.connectDb() is -1:
            return -1

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
            return -1

        finally:
            self.connection.close()

    def getName(self):

        if self.connectDb() is -1:
            return -1

        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT `name` FROM `registered` WHERE id_no=\'" + self.matchedID + "\'"
                cursor.execute(sql)
                result = cursor.fetchone()
                self.matchedName = result["name"]

        except Exception as e:
            print('Error getting Name! \n {!r}, errno is {}'.format(e, e.args[0]))
            return -1

        finally:
            self.connection.close()

    def register(self, id_no, name, phone, email, fpTemplate):

        templatePath = Path(fpTemplate)
        if templatePath.is_file() is False:
            print("Cannot find fingerprint template!")
            return -1

        if self.connectDb() is -1:
            return -2

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
            return -2

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
            return -1

    def compressBMP(self, fileName):
        binary = './nbis/bin/cwsq'
        arguments = ["2.25","wsq",fileName, "-raw_in", "320,480,8"]
        result = self.executeBinary(binary, arguments)
        if result is not '':
            print("Compression error!")
            print(result)
            return -1

    def minutiaeDetect(self, fileName):
        binary = './nbis/bin/mindtct'
        arguments = ["-m1",fileName, fileName[:-4]]
        result = self.executeBinary(binary, arguments)
        if result is not '':
            print("Detection error!")
            print(result)
            return -1
        cleanTemp()

    def matchFingerprints(self, templateOne, templateTwo):
        self.score = 0
        self.splitTemplates(templateTwo)
        scores = None
        binary = './nbis/bin/bozorth3'
        galleryFiles = [os.path.join("temp", 'gallery%d.xyt' % i) for i in range(1,6)]
        arguments = ["-p",templateOne] + galleryFiles
        result = self.executeBinary(binary, arguments)
        scores = re.findall(r'\d+', result)
        for i in range(len(scores)):
            scores[i] = int(scores[i])
        if scores is None or len(scores) is not 5:
            print(result)
            return -1
        else:
            self.score = max(scores)

    def findMatch(self, fileName):
        flag = False;
        indir = './fpData'
        for root, dirs, filenames in os.walk(indir):
            for f in filenames:
                if self.matchFingerprints(fileName, 'fpData/' + f) is -1:
                    return -2
                if self.score > 40:
                    self.matchedID = f[:-4]
                    self.getName()
                    print(self.matchedID)
                    flag = True
                    break
        if flag is False:
            return -1

    def readFingerprint(self,fileName):
        if self.scanFingerprint(fileName + ".bmp") is -1:
            return -1
        self.compressBMP("temp/" + fileName + ".bmp")
        self.minutiaeDetect("temp/" + fileName + ".wsq")
        self.templateLineCount = getNumberOfLines("temp/" + fileName + ".xyt")


    def getFingerprint(self,fileName):
        self.templateLineCount = 0
        while self.templateLineCount < 35:
            if self.readFingerprint(fileName) is -1:
                return -1

    def markAttendance(self):
        if self.getFingerprint("temp") is -1:
            return -1
        ret = self.findMatch('temp/temp.xyt')
        if  ret is -1:
            return -3
        elif ret is -2:
            return -4
        if self.connectDb() is -1:
            return -2
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `attendance` (`userid`) VALUES (%s)"
                cursor.execute(sql, (self.matchedID, ))
            self.connection.commit()

        except Exception as e:
            print("here")
            print('Error inserting into DB!\n {!r}, errno is {}'.format(e, e.args[0]))
            self.connection.close()
            return -2

        finally:
            self.connection.close()

    def combineTemplates(self):
        data = ""
        for x in range(1,6):
            with open("temp/temp" + str(x) + ".xyt", 'r') as myfile:
                data = data + myfile.read()
                if x is not 5:
                    data = data + "<<endoftemplate>>\n"

        open("temp/temp.xyt","w").close()
        with open("temp/temp.xyt","w") as myfile:
            myfile.write(data)

    def splitTemplates(self,fileName):
        data = ""
        with open(fileName, "r") as myfile:
            data = myfile.read()

        for i,template in zip(range(1,6),data.split("\n<<endoftemplate>>\n")):
            open("temp/gallery" + str(i) + ".xyt", 'w').close()
            with open("temp/gallery" + str(i) + ".xyt", 'w') as myfile:
                myfile.write(template)





if __name__ == '__main__':
    o = fpms()
    o.splitTemplates("fpData/B150115CS.xyt")
