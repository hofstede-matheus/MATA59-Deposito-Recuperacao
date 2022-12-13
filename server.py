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

def deposit(conn: socket, filename: str, replicas: int):
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

def restore(conn: socket, filename: str):
  print("Restaurando...")
  print(filename)

  file_path = Path(f"dump/{filename}/{filename}_1")
  fileExists = os.path.isfile(file_path)

  if fileExists:
    data = str.encode('ALREADY_EXISTS')
    conn.sendall(data)
    print("ALREADY_EXISTS")

    with open(file_path, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            print("\n","CHUNK:", bytes_read)
            if not bytes_read:
                break
            conn.sendall(bytes_read)
    print("ok")
  else:
    data = str.encode('NOT_EXISTS')
    conn.sendall(data)
    print("NOT_EXISTS")

def list(conn: socket):
  subfolders = [ f.path.split('/')[1] for f in os.scandir("dump") if f.is_dir() ]
  conn.send(','.join(subfolders).encode())

def error(conn: socket):
  conn.send(f"ERROR".encode())

def start():
  app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
  app_socket.bind((HOST, PORT))

  while True:
    app_socket.listen()
    print("Aguardando conexão do cliente...")
    conn, address = app_socket.accept()

    print('Conectado com:', address)

    data = conn.recv(BUFFER_SIZE)
    decoded_data = data.decode()

    action, filename, replicas = decoded_data.split(SEPARATOR)
    print("Recebido:", action, filename, replicas)

    if action == "TYPE_DEPOSIT":
      deposit(conn, filename, int(replicas))
    elif action == "TYPE_RECOVER":  
      restore(conn, filename)
    elif action == "TYPE_LIST":  
      list(conn)
    else:
      error(conn)

    print("conn.close()")
    conn.close()

start()