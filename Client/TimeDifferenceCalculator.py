import network;
import socket;
import utime;

class TimeDifferenceCalculator:

	def WaitUntilWifiConnected():
		interface = network.WLAN(network.STA_IF)

		while ( not interface.isconnected() ):
			# Wait until the interface is connected to wifi
			pass;

	def GetSecondsSinceGlobalEpoch():
		timeServerHost = "time.nist.gov"
		timeServerPort = 13
		timeRequestHTTPBody = "HEAD / HTTP/1.1\r\nAccept: /\r\nUser-Agent: Mozilla/4.0 (compatible; ESP8266 NodeMcu Lua;)\r\n\r\n"
		timeServerAddressInfo = socket.getaddrinfo(timeServerHost, timeServerPort)
		timeServerAddress = timeServerAddressInfo[0][-1];
		timeServerSocket = socket.socket()
		timeServerSocket.connect(timeServerAddress)
		timeServerSocket.send(bytes(timeRequestHTTPBody, "utf8"))
		receivedData = "";
		while len(receivedData) == 0:
			receivedData = str(timeServerSocket.recv(128), "utf8")
		timeServerSocket.close()
		year = (2000 + int(receivedData[7:9]))
		month = int(receivedData[10:12])
		mday = int(receivedData[13:15])
		hour = int(receivedData[16:18])
		minute = int(receivedData[19:21])
		second = int(receivedData[22:24])
		elapsedSecondsSinceGlobalEpoch = utime.mktime((year, month, mday, hour, minute, second, None, None))

		return elapsedSecondsSinceGlobalEpoch

	def __init__(self):
		self.localEpochGlobalEpochOffsetSeconds = 0
		TimeDifferenceCalculator.WaitUntilWifiConnected()
		elapsedSecondsSinceGlobalEpoch = TimeDifferenceCalculator.GetSecondsSinceGlobalEpoch()
		elapsedSecondsSinceLocalEpoch = utime.time()
		self.localEpochGlobalEpochOffsetSeconds = elapsedSecondsSinceGlobalEpoch - elapsedSecondsSinceLocalEpoch

	def GetMinutesElapsedSince(self, year, month, day, hour, minute, second):
		elapsedSecondsSinceLocalEpoch = utime.time()
		currentTimeSecondsSinceGlobalEpoch = elapsedSecondsSinceLocalEpoch + self.localEpochGlobalEpochOffsetSeconds
		utcTimestamp = (year, month, day, hour, minute, second, None, None)
		
		return ((currentTimeSecondsSinceGlobalEpoch - utime.mktime(utcTimestamp)) / 60)
