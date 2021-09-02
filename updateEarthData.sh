#!/bin/sh
day=$(date +%j)
year=$(date +%Y)
yr=$(date +%y)

echo "[+] NASA's EarthData file: https://cddis.nasa.gov/archive/gnss/data/daily/$year""/brdc/brdc""$day""0.$yr""n.gz"

rm brdc*.Z || echo "[-] No previous EarthData file has been found"

curl -c /tmp/cookie -n -L -o "brdc""$day""0.$yr""n.Z" "https://cddis.nasa.gov/archive/gnss/data/daily/$year""/brdc/brdc""$day""0.$yr""n.gz"

uncompress "brdc""$day""0.$yr""n.Z" 

echo "[+] brdc""$day""0.$yr""n.Z"
