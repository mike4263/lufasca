export BUZWIZZ="50:FA:AB:34:49:2E"
#GATT="gatttool -b 50:FA:AB:34:49:2E "

echo "connect"
sleep 1
echo "char-write-req 0x05 01"
#sleep 2

function invoke_cmd() {
        HANDLE=$1
        echo "char-write-req $HANDLE 107f7f7f7f00"
        echo "char-write-req $HANDLE 1104"
        sleep 12
}

invoke_cmd 0x0003
#echo "disconnect"
#echo "exit"
exit

#echo "disconnect"
