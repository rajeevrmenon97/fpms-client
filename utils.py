import pymysql.cursors
import subprocess


class fpms:
    def __init__(self):
        self.probe = ""
        self.gallery = ""
        self.score = 0

    def register(self, id_no, name, phone, email, fpTemplate):
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='ssl',
                             db='db_ams',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        with open(fpTemplate, 'rb') as f:
            blob = f.read()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT MAX(`serial_no`) FROM `registered`"
                cursor.execute(sql)
                result = cursor.fetchone()
                sno = result["MAX(`serial_no`)"]
                sno = sno + 1
            with connection.cursor() as cursor:
                sql = "INSERT INTO `registered` (`serial_no`, `name`, `id_no`, `phone_no`, `email_id`, `fpData`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (sno, name, id_no, phone, email, blob, ))
            connection.commit()
        finally:
            connection.close()

    def readFingerprint(self, fileName):
        result = subprocess.check_output(['./scanner', fileName])
        





if __name__ == '__main__':
    obj = fpms()
    obj.register("10101","Rajeev",8547088868,"r2m@gmail.com", "f.xyt")
