from socket import *

serverName = '127.0.0.1'
serverPort = 12000

def create_socket_and_send_message(request_message):
    # 소켓 생성
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(request_message.encode('utf-8'))

    # 응답 확인
    recieve_message = clientSocket.recv(65535)
    print(recieve_message.decode())

    clientSocket.close()


while (True):
    url = input("url을 입력해주세요 : ")
    method = input("명령어를 입력하세요 : ")
    if method == 'EXIT':
        break
    
    request_message = method
    request_message += f' {url} HTTP/1.1\r\n'
    request_message += 'Host: 127.0.0.1:12000\r\n'
    request_message += 'Connection:Keep-Alive\r\n'

    if method == 'POST' or method == 'PUT':
        content = input("내용을 입력하세요 : ")
        request_message += 'Content-Type: text/html\r\n'
        request_message += f'Content-Length: {len(content)}\r\n\n{content}'
    else :
        request_message += '\n'

    print('---------------------------------------------')
    # print(request_message)
    create_socket_and_send_message(request_message)
    print('---------------------------------------------\n')