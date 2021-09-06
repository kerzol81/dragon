import requests
from quectel import Quectel
import syslog
import time

ip = ''


class TraccarClient:
    def __init__(self, device_id, server_ip , server_port) -> None:
        self.device_id = device_id
        self.server_ip = server_ip
        self.server_port = server_port
        try:
            self.q = Quectel()
            self.__sendCurrentPostitionInOsmandFormat()
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, f'[+] Traccar-Client initialisation error: {e}')
    
    def __sendCurrentPostitionInOsmandFormat(self):             
        data = {   
                       'id': self.device_id,
                       'lat': self.q.position.latitude,
                       'lon': self.q.position.longitude,
                       'altitude': self.q.position.altitude,
                       'timestamp': self.q.position.timeStamp
                }
        url = f'http://{self.server_ip}:{self.server_port}/'
        
        response = requests.post(url, data = data, timeout=3)
        if response.status_code == 200:
            syslog.syslog(syslog.LOG_INFO, '[+] Position sent to Traccar')
        else:
            syslog.syslog(syslog.LOG_ERR, f'[-] Traccar-Client error while sending position')

        
if __name__ == '__main__':

    print('[+] Starting Traccar-Client service ...')
    rate = 60
    while True:
        traccar = TraccarClient(device_id='Dragon01', server_ip=ip, server_port=5055)
        time.sleep(rate)
        traccar = None
