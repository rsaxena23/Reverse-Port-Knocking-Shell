import sys
import socket
import time

def knock(serverURL,configFile):
    fp = open(configFile)

    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for line in fp:
        try:
            time.sleep(2)
            s.connect((serverURL,int(line)))
            s.shutdown(1)
        except socket.error, msg:
            pass
        print 'Connected',serverURL,line
    s.close()
    print 'Done'


if __name__=='__main__':
    if len(sys.argv)>2:
        configFile = str(sys.argv[1])
        serverURL = str(sys.argv[2])
        knock(serverURL,configFile)
    else:
        print 'Not enough parameters'
        exit()
