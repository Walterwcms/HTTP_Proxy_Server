from socket import *
import requests

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(("127.0.0.1", 8889))
serversocket.listen(100)

print('Servidor iniciado, esperando clientes . . .')

while True:

    clienteconnect, addr = serversocket.accept()
    print ('recebendo coneccao de:', addr)

    message = clienteconnect.recv(1024)
    message = message.decode()
    filename = message.split()[1].partition("/")[2]
    print ("pagina requisitada pelo cliente: ",filename)


    #---------------------------------verificando se o arquivo existe no servidor PROXY (CASH)--------------------------
    fileExist = "false"
    try:
        filetouse = "/" + filename
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        print(filename," foi encontrado.")

        clienteconnect.send("HTTP/1.0 200 OK\r\n".encode())
        clienteconnect.send("Content-Type:text/html\r\n".encode())

        for i in range(0, len(outputdata)):
            clienteconnect.send(outputdata[i].encode())
            print('enviando dados ao cliente')

    #--------------------------------caso nao encontrar o arquivo no servidor PROXY (CASH)------------------------------
    except IOError:

        if fileExist == "false":
            #------------CONECTADO COM O SERVIDOR-----------
            try:
                response = requests.get("http://ola.com")
                clienteconnect.send(response.text.encode())
                print("pagina enviada")

            except:
                print ("Illegal request")



        else:
            # HTTP response message for file not found
            clienteconnect.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode())
            clienteconnect.send("Content-Type:text/html\r\n".encode())
            clienteconnect.send("\r\n".encode())

    # Close the client and the server sockets
    clienteconnect.close()
serversocket.close()