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
    print("Lista...")
    print("Lista de arquivos:")
    app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_socket.connect((HOST, PORT))

    action = "TYPE_LIST"
    app_socket.send(f"{action}{SEPARATOR}-{SEPARATOR}0".encode())
    message, _ = app_socket.recvfrom(BUFFER_SIZE)

    decoded_message = message.decode()
    print(decoded_message)

  def deposit_file(nome_do_arquivo: str, nivel_de_tolerancia: int):
    print("Deposita...")
    app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_socket.connect((HOST, PORT))

    action = "TYPE_DEPOSIT"
    app_socket.send(f"{action}{SEPARATOR}{nome_do_arquivo}{SEPARATOR}{nivel_de_tolerancia}".encode())
    message, _ = app_socket.recvfrom(BUFFER_SIZE)

    decoded_message = message.decode()
    print(decoded_message)

    if decoded_message == "ALREADY_EXISTS":
      app_socket.close()
      return
    else:

      with open(nome_do_arquivo, "rb") as f:
          while True:
              bytes_read = f.read(BUFFER_SIZE)
              if not bytes_read:
                break
              app_socket.sendall(bytes_read)

      app_socket.close()

  def recover_file(nome_do_arquivo: str):
    print("Recupera...")
    app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_socket.connect((HOST, PORT))

    action = "TYPE_RECOVER"
    app_socket.send(f"{action}{SEPARATOR}{nome_do_arquivo}{SEPARATOR}{0}".encode())
    message, _ = app_socket.recvfrom(BUFFER_SIZE)
    decoded_message = message.decode()
    print(decoded_message)

    if decoded_message == "NOT_EXISTS":
      app_socket.close()
      return
    else:

      with open(f"restore/{nome_do_arquivo}", "wb") as f:
          while True:
              bytes_read = app_socket.recv(BUFFER_SIZE)
              print("\n","CHUNK:", bytes_read)
              if not bytes_read:
                break
              f.write(bytes_read)
      print("*")
      app_socket.close()