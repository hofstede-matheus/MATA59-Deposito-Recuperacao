import os

from proxy import Proxy

def clear_line():
  os.system('cls' if os.name == 'nt' else 'clear')

def parse_mode():
  mode = input("Selecione um modo: \n1 - Modo Depósito \n2 - Modo Recuperação \n")
  if mode == "1":
    init_deposit_mode()

  elif mode == "2":
    init_recovery_mode()

  else:
    print("Modo inválido, saindo...")
    exit()


def init_deposit_mode():
  clear_line()
  print("Modo Depósito")
  file_name = input("Nome do arquivo (na pasta atual):")
  tolerance_level = input("Nível de toleância (quantidade de répicas):")

  Proxy.deposit_file(file_name, tolerance_level)



def init_recovery_mode():
  clear_line()
  # recuperará com formato: copy_ + $nome_original
  print("Modo Recuperação")
  
  Proxy.get_file_list()
  file_name = input("Nome do arquivo (na pasta atual):")

  Proxy.recover_file(file_name)



# start here
print("init")

while (True):
  # clear_line()
  parse_mode()