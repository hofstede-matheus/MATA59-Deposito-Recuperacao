import socket
from pathlib import Path
import os
import shutil
import os.path
import time

HOST = os.environ.get('SERVER_URL', 'localhost')
print(HOST)
PORT = 5959
BUFFER_SIZE = 1024
SEPARATOR = "|"

def start():
  app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
  app_socket.bind((HOST, PORT))
  app_socket.listen()

  print("Aguardando conexão do cliente...")
  conn, address = app_socket.accept()

  print('Conectado com:', address)

  data = conn.recv(BUFFER_SIZE)
  decoded_data = data.decode()

  action, filename, filesize, replicas = decoded_data.split(SEPARATOR)
  print("Recebido:", action, filename, filesize, replicas)

  file_path = Path(f"dump/{filename}/{filename}_1")

  fileExists = os.path.isfile(file_path)

  if fileExists:
    data = str.encode('ALREADY_EXISTS')
    conn.sendall(data)
    print("ALREADY_EXISTS")

    for i in range(2, int(replicas)+1):
      shutil.copy(file_path, Path(f"dump/{filename}/{filename}_{i}"))
  else:
    data = str.encode('NOT_EXISTS')
    conn.sendall(data)
    print("NOT_EXISTS")

    os.makedirs(f"dump/{filename}/", exist_ok=True)

    with open(file_path, "wb") as f:
        while True:
            bytes_read = conn.recv(BUFFER_SIZE)
            print("\n","CHUNK:", bytes_read)
            if not bytes_read:    
                break
            f.write(bytes_read)
    # replicate
    for i in range(2, int(replicas)+1):
        shutil.copy(file_path, Path(f"dump/{filename}/{filename}_{i}"))


  conn.close()
  app_socket.close()
  time.sleep(1)
  start()

start()