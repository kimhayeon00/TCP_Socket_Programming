from socket import *
import time

import sys

StatusCode = {'CONTINUE':'100', 'OK':'200', 'CREATED':'201', 'BAD REQUEST':'400', 'NOT FOUND':'404'}
# 상태를 나타내는 코드
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
# TCP 서버 소켓 생성
serverSocket.bind(('127.0.0.1',serverPort))
# 시스템간 패킷 전달을 위한 bind

serverSocket.listen(1)
# 서버 요청 받기 시작
print("The server is running")
    
def GET(status = 'OK'):
    f = open('./test.txt','r')
    content = f.read()     
    f.close()
    return resMessage(status,content)

def HEAD():
    return resMessage('CONTINUE', '')

def POST(content):
    f = open('./test.txt','a')
    f.write(content)
    f.write('\n')
    f.close()
    return GET()

def PUT(content):
    try:
        f = open('./test.txt','r+')
        line = f.read()
        line = line.split()
    
        for i in line:
            if content == i :
                f.close()
                return GET()
            
        f.write(content)
        f.write('\n')
        f.close()
        return GET('CREATED')   
            

    except:
        return resMessage('BAD REQUEST','')
    

def resMessage(status,content=''):
    print("---res---")
    res = ""
    date = time.strftime('%a, %d %b %Y %H:%M:%S KST', time.localtime(time.time()))
    res += f"HTTP/1.1 {StatusCode[status]} {status}\r\n"
    res += 'Content-Type: text/html\r\n'
    res += f'Content-Length: {len(content)}\r\n'
    res += f'Date: {date}\r\n\n'
    res += f'{content}'
    return res
    

while True:
    connectionSocket, addr = serverSocket.accept()

    message = connectionSocket.recv(65535).decode()
    request_headers = message.split()
    method = request_headers[0]
    print("---Success server---\n")
    print(message)
    if request_headers[2] == 'HTTP/1.1' and method in ['GET', 'HEAD', 'POST', 'PUT']:
        #주소가 맞는 경우
        print("---method in---\n")
        if request_headers[1] in ['/','/index.html', './index.html']:
            if method == 'GET' : res = GET()
            elif method == 'HEAD' : res = HEAD()
            elif method == 'POST': res = POST(request_headers[-1])
            elif method == 'PUT': res = PUT(request_headers[-1])
            
        else:
            res = resMessage('NOT FOUND')
        connectionSocket.send(res.encode('utf-8'))
    else:
        res = resMessage('NOT FOUND')
        connectionSocket.send(res.encode('utf-8'))
        break
