from socket import *
import socket
import threading
import logging
import time
from datetime import datetime
import sys

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 45000)
    logging.warning(f"membuka socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] mengirim {message}")
        sock.sendall(message.encode())
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(32)
            amount_received += len(data)
            logging.warning(f"[DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning("closing")
        sock.close()
    return

def create_thread():
    t = threading.Thread(target=kirim_data)
    t.start()
    t.join()

if __name__=="__main__":
    count = 0
    start = time.time()
    
    while time.time() - start < 60:
        create_thread()
        count += 1
        
    start_time = datetime.fromtimestamp(start)
    finish_time = datetime.fromtimestamp(time.time())
    logging.warning(f"Waktu mulai: {start_time}")
    logging.warning(f"Waktu selesai: {finish_time}")
    logging.warning(f"Jumlah threads dibuat: {count}")

# Jalankan 'python3 client_thread.py' di terminal