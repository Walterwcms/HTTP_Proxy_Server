from socket import *

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
            #------------CRIANDO UM SOCKET EM SERVIDOR PROXY-----------
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
                # Read the response into buffer
                buff = fileobj.readlines()
                # Create a new file in the cache for the requested file. Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                for line in buff:
                    tmpFile.write(line.encode())
                    clienteconnect.send(line.encode())

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