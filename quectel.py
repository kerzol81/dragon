import subprocess
from datetime import datetime
import sqlite3
import syslog
import time

class DBHandler:
    global db_file 
    db_file = '/home/dragon/gps.db'

    global max_rows
    max_rows = 100000
    
    @staticmethod
    def createDB():
        try:
            
            con = sqlite3.connect(db_file)
            cur = con.cursor()
            sql = """CREATE TABLE IF NOT EXISTS "positions" (
	                    "timeStamp"	TEXT UNIQUE,
	                    "latitude"	TEXT,
	                    "longitude"	TEXT,
	                    "altitude"	TEXT,
	                    PRIMARY KEY("timeStamp")
                )"""

            cur.execute(sql)
            con.close()
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, f'[-] db creation error: {e}')
            pass
        
        try:
            subprocess.getoutput(f'chmod 777 {db_file}')
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, f'[-] chmod error: {e}')
            pass
    

    @staticmethod
    def insert(position):              
        try:
            con = sqlite3.connect(db_file)
            cur = con.cursor()

            number_of_rows = cur.execute('SELECT count(*) from positions;').fetchone()[0]                  
            if number_of_rows >= max_rows:
                cur.execute('DELETE FROM positions;')
                con.commit()
                syslog.syslog(syslog.LOG_INFO, f'[+] Database truncated when records reached: {max_rows} rows.')

            sql = 'INSERT INTO positions (timeStamp, latitude, longitude, altitude) VALUES ("{}","{}","{}","{}");'.format(str(position.timeStamp), str(position.latitude)[:10], str(position.longitude)[:10], str(position.altitude))
            cur.execute(sql)
            con.commit()
            con.close()
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, f'[-] sql insert error: {e}')
            pass
    
       

class Position:
    def __init__(self, timeStamp, latitude, longitude, altitude) -> None:
        self.timeStamp = timeStamp
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class Quectel:
    def __init__(self) -> None:  
        self.position = self.__getPosition()

    def __turnOnGPS(self):
        command = 'mmcli -m 0 --command="AT+QGPS=1"'
        response = subprocess.getoutput(command)
        if response.__contains__('error'):
            syslog.syslog(syslog.LOG_ERR, '[-] error: could not turn on gps')
        syslog.syslog(syslog.LOG_INFO, '[+] GPS turned on')
              
           
    def __getPosition(self):
        response = subprocess.getoutput('mmcli -m 0 --command="AT+QGPSLOC?"')
        if response.__contains__('+QGPSLOC'):
            data = response.split(',')[1][:-1]
            latitude = (float(data[:2]) + (float(data[2:]) / 60.0))
            data = response.split(',')[2][:-1]
            longitude = (float(data[1:3]) + (float(data[3:]) / 60.0))  
            altitude = float(response.split(',')[4])
            p = Position(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), latitude, longitude, altitude)
            syslog.syslog(syslog.LOG_INFO, f'[+] GPS: Latitude: {p.latitude}, Longitude: {p.longitude}, Altitude: {p.altitude}')
            return p
        syslog.syslog(syslog.LOG_ERR, '[-] error: no GPS data')
        self.__turnOnGPS()

   

if __name__ == '__main__':

    print('[+] Starting Quectel GPS service ...')
    rate = 5
    while True:            
        q = Quectel()
        DBHandler.createDB()
        DBHandler.insert(q.position)
        syslog.syslog(syslog.LOG_INFO, f'[+] GPS refresh : {rate} seconds')
        q = None
        time.sleep(rate)
        
