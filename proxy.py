import os
import socket
import time

HOST = os.environ.get('SERVER_URL', 'localhost')


print(HOST)
PORT = 5959
SEPARATOR = "|"
BUFFER_SIZE = 1024


class Proxy:
  def get_file_list():
    print("Lista de arquivos:")
    subfolders = [ f.path.split('/')[1] for f in os.scandir("dump") if f.is_dir() ]
    print(subfolders)

  def deposit_file(nome_do_arquivo: str, nivel_de_tolerancia: int):
    print("Deposita...")
    app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(HOST)
    app_socket.connect((HOST, PORT))

    action = "TYPE_DEPOSIT"
    filesize = os.path.getsize(nome_do_arquivo)

    app_socket.send(f"{action}{SEPARATOR}{nome_do_arquivo}{SEPARATOR}{filesize}{SEPARATOR}{nivel_de_tolerancia}".encode())
    message, _ = app_socket.recvfrom(BUFFER_SIZE)

    decoded_message = message.decode()

    print("arquivos já existe?", decoded_message)

    if decoded_message == "ALREADY_EXISTS":
      print("Arquivo já existe, saindo...")
      app_socket.close()
      return
    
    time.sleep(1)

    with open(nome_do_arquivo, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
              break
            app_socket.sendall(bytes_read)

    app_socket.close()

  def recover_file(nome_do_arquivo: str):
    print("Recupera...")