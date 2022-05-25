


import threading
from socket import *


serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 80
serverSocket.bind(("192.168.2.6", serverPort))
serverSocket.listen(1)



#-----------------------------------------------------------------------------------------------------------------------
def newConeccao(connectionSocket,addr):

    print("\nCliente " + str(addr) + "conectado")
    try:
        message = connectionSocket.recv(1024).decode("unicode_escape")
        # ----------------se cliente desconectou-----------------------------
        if (message == 0):
            return 0
        #--------------------------------------------------------------------

        #----------ler o arquivo que foi requizitado--------------------------
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        #---------------------------------------------------------------------


        connectionSocket.close()

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()
#-----------------------------------------------------------------------------------------------------------------------


#-----------------------Apenas uma funcao para desligar o servidor------------------------------------------------------
def DesligarServidor(serverSocket):
    if(input() == "desligar"):
        serverSocket.close()
        print(" **** Servidor DESLIGADO ****")
        exit(1)
        print("exit ignorado na funcao Desligar servidor")

#-----------------------------------------------------------------------------------------------------------------------




print("* ------ Servidor iniciado ------ *")
funcao_desligar_servidor = threading.Thread(target=DesligarServidor, args=[serverSocket])
funcao_desligar_servidor.start()

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        x = threading.Thread(target=newConeccao, args=[connectionSocket, addr])
        x.start()
    except:
        #encerra quando nao conseguir executar serverSocket.accept()
        exit(0)


