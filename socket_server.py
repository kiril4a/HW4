import socket
import json
from datetime import datetime
import os

def start_socket_server():
    if not os.path.exists('storage'):
        os.makedirs('storage')

    data_file = 'storage/data.json'
    if not os.path.exists(data_file):
        with open(data_file, 'w') as f:
            json.dump({}, f)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 5000))

    while True:
        message, _ = server_socket.recvfrom(1024)
        message = message.decode('utf-8')
        message_dict = json.loads(message)
        
        timestamp = str(datetime.now())
        with open(data_file, 'r+') as f:
            data = json.load(f)
            data[timestamp] = message_dict
            f.seek(0)
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    start_socket_server()
