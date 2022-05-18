import socket
import threading
import time
import mysql.connector

# Inicia servidor
while True:
    try:
        HOST = input("Host: ")
        PORT = int(input("Port: "))
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((HOST,PORT))
        server.listen()
        print(f'Server is Up and Listening on {HOST}:{PORT} !!')
        break
    except:
        print(f'Unable to start server, try another IP and port!!')
        pass

# Faz conexão com o banco
while True:
    try:
        USERdb = input("User DB: ")
        PASSWORDdb = input("Password DB: ")
        con = mysql.connector.connect(host='localhost', database='APS_Ambiental',user=USERdb,password=PASSWORDdb)
        print(f'Data base is conected!!')
        break
    except:
        print(f'Invalid database username or password!!')
        pass

# Guarda endereço ip e nome dos usuarios
clients = []
usernames = []

# Inicia conexão Server-Client
def initialConnection():
    global clients
    global usernames
    while True:
        try:
            client, address = server.accept()
            user_thread = threading.Thread(target=ClientMessages,args=(client, address))
            user_thread.start()
            print(f"New Connetion: {str(address)}")
        except:
            pass

# Recebe mensagens do usuario
def ClientMessages(client, address):
    global usernames
    global clients
    while True:
        try:
            # Mensagem recebida do cliente
            msg = (client.recv(2048).decode('UTF-8'))
            
            # Se a mensagem vier com "#!usuario!##!senha!# " no inicio será considerada como dados de login para validação
            if msg[:21] == "#!usuario!##!senha!# ":
                msg = msg[21:]
                username = msg.split("  :  ")[0]
                password = msg.split("  :  ")[1]
                response = UserValidation(username, password, client)
                if response == 0:
                    client.send('CONFIRMED USER'.encode('UTF-8'))
                    usernames.append(username)
                    clients.append(client)
                    print(f"{str(username)} completed connection via login!!")
                elif response == 1:
                    client.send('USER IS ALREADY CONNECTED'.encode('UTF-8'))
                elif response == 2:
                    client.send('USER DOES NOT EXIST'.encode('UTF-8'))
            
            elif msg[:20] == "#!cadastroDespejo!# ":
                msg = msg[20:]
                empresa = msg.split("  :  ")[0]
                cnpj = msg.split("  :  ")[1]
                tipo = msg.split("  :  ")[2]
                quantidade = msg.split("  :  ")[3]
                regiao = msg.split("  :  ")[4]
                tipo = int(BuscaTipoDespejo(tipo))
                empresa = int(BuscaEmpresa(empresa))
                quantidade = int(BuscaQuantidade(quantidade))
                regiao = int(BuscaRegiao(regiao))
                cnpj = int(BuscaCNPJ(cnpj))
        except:
            pass


# Valida o úsuario e senha
def UserValidation(user, password, client):
    global con
    global usernames
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM USUARIOS WHERE USUARIO = '{user}' AND SENHA = '{password}';")
        result = cursor.fetchall()
        if len(result) != 0:
            if not user in usernames:
                return 0
            else:
                return 1
        else:
            return 2


def cadastroDespejo(empresa, cnpj, tipo, quantidade, regiao):
    global con
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f'INSERT INTO DESPEJOS(ID_DESPEJOS, EMPRESA, TIPO_DESPEJO, REGIAO, DESCRICAO, QUANTIDADE) VALUES (null, 6, 1, "BARUERI", "LIXO DE PEQUENO PORTE LIBERADO EM BARUERI", 100);')
        result = cursor.fetchall()


def BuscaTipoDespejo(tipo):
    global con
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f"SELECT ID_TIPO FROM TIPOS WHERE VALOR = '{tipo}';")
        result = cursor.fetchall()
        return str(result[0]).replace('(','').replace(')','').split(',')[0].replace(' '','').replace(''', '')


def BuscaEmpresa(empresa):
    global con
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f"SELECT ID_EMPRESA FROM EMPRESAS WHERE RAZAO_SOCIAL = '{empresa}' ;")
        result = cursor.fetchall()
        return str(result[0]).replace('(','').replace(')','').split(',')[0].replace(' '','').replace(''', '')


def BuscaQuantidade(quantidade):
    global con
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f" = '{quantidade}' ;")
        result = cursor.fetchall()
        return str(result[0]).replace('(','').replace(')','').split(',')[0].replace(' '','').replace(''', '')


def BuscaRegiao(regiao):
    global con
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f" = '{regiao}' ;")
        result = cursor.fetchall()
        return str(result[0]).replace('(','').replace(')','').split(',')[0].replace(' '','').replace(''', '')


def BuscaCNPJ(cnpj):
    global con
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f" = '{cnpj}' ;")
        result = cursor.fetchall()
        return str(result[0]).replace('(','').replace(')','').split(',')[0].replace(' '','').replace(''', '')

########### INICIO (AGUARDA A CONEXÃO COM O CLIENTE) ##############
initialConnection()
#################################






















##############################



"""
def globalMessage(message):
    for client in clients:
        if usernames[clients.index(client)] != message[:len(usernames[clients.index(client)])].decode('UTF-8'):
            client.send(message)
"""


######################


""" 
def getDB(message):
    for client in clients:
        if usernames[clients.index(client)] == message[:len(usernames[clients.index(client)])].decode('UTF-8'):
            message = message.decode('UTF-8')[len(usernames[clients.index(client)])+2:].encode('UTF-8')
            client.send(message)
"""


######################



""" 
def handleMessages(client):
    while True:
        try:
            receiveMessageFromClient = client.recv(2048).decode('UTF-8')
            if receiveMessageFromClient[:21] == "#!usuario!##!senha!# ":
                msg = receiveMessageFromClient[21:]
                user = msg.split("  :  ")[0]
                password = msg.split("  :  ")[1]
                UserValidation(user, password, client)
            #if receiveMessageFromClient[:5] == "getid":
            #    try:
            #        dadosDB(receiveMessageFromClient[6:], client)
            #    except:
            #        print(f"não achou o ID solicitado por {usernames[clients.index(client)]}")
            else:
                globalMessage(f'{usernames[clients.index(client)]}: {receiveMessageFromClient}'.encode('UTF-8'))
        except:
            clientLeaved = clients.index(client)
            client.close()
            clients.remove(clients[clientLeaved])
            clientLeavedUsername = usernames[clientLeaved]
            print(f'{clientLeavedUsername} has left the chat...')
            globalMessage(f'{clientLeavedUsername} has left us...'.encode('UTF-8'))
            usernames.remove(clientLeavedUsername)
"""

###########################

""" 
def dadosDB(id, client):
    con = mysql.connector.connect(host='localhost', database='MYSQL_PYTHON',user='root',password='root')
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM Tabela_Dados WHERE ID = {id};")
        result = cursor.fetchall()
        if len(result) == 1:
            getDB(f'{usernames[clients.index(client)]}: || {result[0][0]} || {result[0][1]} || {result[0][2]} || {result[0][3]} || {result[0][4]} || {result[0][5]} ||'.encode('UTF-8'))
        else:
            getDB(f'{usernames[clients.index(client)]}: ID inválido'.encode('UTF-8'))
"""
