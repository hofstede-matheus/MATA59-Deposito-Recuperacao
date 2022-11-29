# MATA59-Deposito-Recuperacao

https://drive.google.com/file/d/1suVbp2qnNidwpGH6T5fPuxLTXAllS3ym/view

## Referências

https://docs.python.org/3/library/multiprocessing.html
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/argparse.html



- Modos:
	- Depósito
		- input
			- nome do arquivo
			- quantidade de réplicas
	- Recuperação
		- input
			- nome do arquivo



✅ Persistência em disco

✅ Uso de sockets para mensagens e transferências de arquivo

✅ Atualização de replicas para arquivos que já existem


```
docker-compose run --rm --name mata59-server server
docker-compose run --rm --name mata59-client client
``` 
OU

```
python3 server.py
python3 main.py
``` 