from copy import deepcopy
import socket
from threading import Thread

class net():
	def __init__(self):
		self.s = []
		self.lastport = 27000
		self.ports = []
		ip = None
		self.names = []
		self.messages = []
	def close(self,name):
		index = self.names.index(name)
		self.s[index].close()
		#del self.messages[index][:]
		self.messages[index] = False
	def close_all(self):
		for index in range(len(self.s)):
			self.close(self.names[index])
		self.__init__()
	def recv(self,name):
		index = self.names.index(name)
		#toreturn = deepcopy(self.messages[index])
		#toreturn = self.messages[index]
		#del self.messages[index][:]
		#return toreturn
		return self.messages[index]
	def save_recived_data(self,name):
		index = self.names.index(name)
		while True:
			data,addr = self.s[index].recvfrom(1024)
			if addr[0] == self.ip:
				#self.messages[index].append(data.decode('utf-8'))
				self.messages[index] = data.decode('utf-8')
			else:
				print('Bad sender(ip): ',end='')
				print(addr)
	def send(self,name,message):
		index = self.names.index(name)
		self.s[index].sendto(message.encode('utf-8'),(self.ip,self.ports[index]))
	def set_ip(self,ip):
		self.ip = ip
	def listen(self,name):
		port = self.lastport+1-1
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.bind(('',port))
		self.s.append(s)
		self.ports.append(port)
		self.lastport += 1

		if name in self.names:
			raise "Name already added"
		self.names.append(name)
		#self.messages.append([])
		self.messages.append(False)

		Thread(target=self.save_recived_data,args=[name]).start()		
net = net()
