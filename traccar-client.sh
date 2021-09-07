#!/bin/bash

traccar_ip='172.33.33.200'
traccar_port='5055'
id='pc001'
lat='47.1'
lon='19.1'
altitude='3'

curl -X POST -H 'content-length: 128' http://$traccar_ip:$traccar_port/?id=$id&lat=$lat&lon=$lon&altitude=$altitude&timestamp=$(date +"%Y-%m-%d %H:%M:%S") || logger '[-] Traccar Client: error while sending GPS data'; exit 1

exit 0
