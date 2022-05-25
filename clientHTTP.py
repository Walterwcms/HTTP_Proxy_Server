import requests

import sys

if __name__ == "__main__":
    arquivo = str(sys.argv[3]).replace(".html","")
    porta = sys.argv[2]
    if(porta != "80"):
        print('\033[91m' + "Erro na porta. Digita uma porta valida para o conectar no Webserver" + '\033[0m')
        exit(-1)

    ip =  str(sys.argv[1])

    try:
        r = requests.get("http://"+ip+"/"+arquivo+".html")
        print(r.text)
        print('\033[92m' + "Conectado no servidor " + '\033[0m')
    except:
        print('\033[91m' + "Não foi possível conectar-se a esta rede" + '\033[0m')