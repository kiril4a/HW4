from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import socket
import threading
import json
from datetime import datetime
import os

app = Flask(__name__)

# Створення директорії storage і файлу data.json, якщо вони не існують
if not os.path.exists('storage'):
    os.makedirs('storage')
if not os.path.exists('storage/data.json'):
    with open('storage/data.json', 'w') as f:
        json.dump({}, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message.html')
def message():
    return render_template('message.html')

@app.route('/message', methods=['POST'])
def send_message():
    try:
        username = request.form['username']
        message = request.form['message']
        
        # Надсилання даних на UDP сервер
        data = json.dumps({'username': username, 'message': message})
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data.encode('utf-8'), ('localhost', 5000))
        
        # Після успішної відправки повідомлення перенаправляємо користувача на головну сторінку
        return redirect('/')
    except Exception as e:
        print(f"Error in send_message: {e}")
        return render_template('error.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 5000))
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message_data = json.loads(data.decode('utf-8'))
            
            # Отримання поточного часу
            current_time = datetime.now().isoformat()
            
            # Зчитування існуючих даних
            with open('storage/data.json', 'r') as f:
                existing_data = json.load(f)
            
            # Додавання нового повідомлення
            existing_data[current_time] = message_data
            
            # Запис оновлених даних
            with open('storage/data.json', 'w') as f:
                json.dump(existing_data, f, indent=4)
        except Exception as e:
            print(f"Error in UDP server: {e}")

if __name__ == '__main__':
    threading.Thread(target=udp_server).start()
    app.run(port=3000)
