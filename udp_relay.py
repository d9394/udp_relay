#!/usr/bin/python
#coding=utf8
from socket import * 
import threading
import datetime,time
import sys

debug = True

if sys.getdefaultencoding() != 'utf8' :
	reload(sys)
	sys.setdefaultencoding('utf8')
config={
	"car_server":("127.0.0.1:50025","192.168.100.1:50025"),
	"aprs_server":("192.168.100.1:14580","aprs.hellocq.net:14580"),
	"relay_aprs_id":("BB7IS-5","BB7IS-7","BB7IS-6"),
	"relay_car_id":("00000000","00000001")
}

def car_udp():
	try:
		mSocket = socket(AF_INET,SOCK_DGRAM)
		mSocket.bind(("",5025)) 
	except :
		print("bind 5025 error")
	
	while True:
		revcData, (remoteHost, remotePort) = mSocket.recvfrom(1024)
#		revcData="$SJHX,289594937E7E00007E7E020301803955352401161766210162090501010108191625132655351234567F12345F1"
		revcData=revcData.decode("utf-8").strip()
		print("Recv CAR UDP: %s, from %s:%s" % (revcData,remoteHost, remotePort))
#		mSocket.sendto("OK", (remoteHost, remotePort))
		if len(revcData)>0 :
			send_udp("car_server", revcData)
	mSocket.close()

def aprs_udp():
	try:
		mSocket = socket(AF_INET,SOCK_DGRAM)
		mSocket.bind(("",14580))
	except :
		print("bind 14580 error")
	while True:
		revcData, (remoteHost, remotePort) = mSocket.recvfrom(1024)
		revcData=revcData.decode("utf-8").strip()
#		mSocket.sendto("OK", (remoteHost, remotePort))
		print("Recv APRS UDP: %s, from %s:%s" % (revcData,remoteHost, remotePort))
		if len(revcData)>0 :
			send_udp("aprs_server", revcData)
	mSocket.close()

def send_udp(type,msg):
	nmSocket = socket(AF_INET,SOCK_DGRAM)
	for ii in config[type]:
		jj = ii.strip().split(":")
		ip_port = (gethostbyname(jj[0]), int(jj[1]))
		nmSocket.sendto(msg.encode('utf-8'),ip_port)
		print("Send (%s) %s to %s" % (type, msg, ii))
	nmSocket.close()
		
if __name__ == '__main__':
	t1 = threading.Thread(target=car_udp, name='car_udp_server')  # 线程对象.
	t2 = threading.Thread(target=aprs_udp, name='aprs_udp_server')  # 线程对象.
#	print("==Service Started== %s" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	while True:
		if not t1.isAlive() :
			print("Start car_udp_server %s" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
			t1.start()
		if not t2.isAlive() :
			print("Start aprs_udp_server %s" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
			t2.start()
		time.sleep(300)
