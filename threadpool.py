from socket import *
import socket
import logging
import time
from datetime import datetime
import sys
from concurrent.futures import ThreadPoolExecutor

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

if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        start = time.time()
        count = 0
        futures = set()

        while time.time() - start < 60:
            future = executor.submit(kirim_data)
            futures.add(future)
            completed_futures = {f for f in futures if f.done()}
            count += len(completed_futures)
            futures -= completed_futures

        for future in futures:
            future.result()
            
        start_time = datetime.fromtimestamp(start)
        finish_time = datetime.fromtimestamp(time.time())
        logging.warning(f"Waktu mulai: {start_time}")
        logging.warning(f"Waktu selesai: {finish_time}")
        logging.warning(f"Jumlah request terkirim: {count}")

# Jalankan 'python3 threadpool.py' di terminal