from socket import *
import socket
import logging
from datetime import datetime
import time
import sys
from multiprocessing import Process

time.sleep(5)

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 45000)
    logging.warning(f"membuka socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME\r\n'
        logging.warning(f"[CLIENT] sending {message}")
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

def create_process():
    p = Process(target=kirim_data)
    p.start()
    p.join()
    
if __name__ == '__main__':
    start = time.time()
    count = 0
    
    while time.time() - start < 60:
        create_process()
        count += 1
        
    start_time = datetime.fromtimestamp(start)
    finish_time = datetime.fromtimestamp(time.time())
    logging.warning(f"Waktu mulai: {start_time}")
    logging.warning(f"Waktu selesai: {finish_time}")
    logging.warning(f"Jumlah process dibuat: {count}")

# Jalankan 'python3 process.py' di terminal