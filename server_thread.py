from socket import *
import socket
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address,server):
		self.connection = connection
		self.address = address
		self.server = server
		threading.Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(32)
			if data:
				decoded_data = data.decode('utf-8')
				clean_data = decoded_data.strip()
				logging.warning(f"[SERVER] menerima pesan {decoded_data}")
				if data.startswith(b'TIME') and data.endswith(b'\r\n'):
					current_time_formatted = time.strftime("%H:%M:%S")
					respon = f"JAM {current_time_formatted}\r\n"
					logging.warning(f"[SERVER] mengirim respon {respon}")
					self.connection.sendall(respon.encode('utf-8'))
					self.server.count_responses()
				else:
					break
			else:
				break
		self.connection.close()

class TimeServer(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.response_count = 0
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			clt = ProcessTheClient(self.connection, self.client_address, self)
			clt.start()
			self.the_clients.append(clt)
            
	def count_responses(self):
		self.response_count += 1
		logging.warning(f"Jumlah response terkirim: {self.response_count}")
        
def main():
	svr = TimeServer()
	svr.start()

if __name__=="__main__":
	main()

# Jalankan 'python3 server_thread.py' di terminal