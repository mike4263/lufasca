#!/usr/bin/env python
from gattlib import DiscoveryService, GATTRequester, GATTResponse
from time import sleep

BUZWIZZ = "50:FA:AB:34:49:2E"

while(1):
    service = DiscoveryService("hci0")
    devices = service.discover(2)

    for address, name in devices.items():
        print("name: {}, address: {}".format(name, address))

    sleep(2)

    req = GATTRequester(BUZWIZZ, False)
    req.connect(True)
    req.write_by_handle(0x05,bytes([1]))
    req.write_by_handle(0x0003,bytes([16,127,127,127,127,0]))
    req.write_by_handle(0x0003,bytes([17,4]))

    sleep(2)
    req.check_status()
    req.disconnect()


#GATT="gatttool -b 50:FA:AB:34:49:2E "
#echo "connect"
#sleep 1
#echo "char-write-req 0x05 01"
#function invoke_cmd() {
#        HANDLE=$1
#        echo "char-write-req $HANDLE 107f7f7f7f00"
#        echo "char-write-req $HANDLE 1104"
#        sleep 12
#}
#
#invoke_cmd 0x0003
##echo "disconnect"
##echo "exit"
#exit
#
##echo "disconnect"
