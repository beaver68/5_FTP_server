import socket

def work():
    print('''pwd - показывает название рабочей папки
        ls - показывает содержимое рабочей папки
        cat <filename> - показывает содержимое рабочей папки
        mkdir <filename> - создает директорию
        cd <filename> - переходит в указанную директорию
        cd .. - возвращает на 1 уровень выше
        whoami - возвращает логин текущего пользователя
        rename <old> <new> - переименовывает файл
        rm <filename> - удаляет файл находящийся в папке
        rmdir <name> - удаляет указанную директорию и все файлы в ней ''')
    while True:
        #print('Aviable commands: ls, pwd, cat <filename>')
        request = input('> ')
        if request.upper() == 'EXIT':
            break
        sock.send((request.encode()))
        msg = sock.recv(1024).decode()
        print(msg)


host = 'localhost'
port = 9090

sock = socket.socket()
sock.connect((host, port))

while True: #while authorization
    msg = sock.recv(1024).decode()
    if msg.lower() == 'authorization is done!':
        work()
        break
    print(msg)
    request = input('> ')
    if request.upper() == 'EXIT':
        break


    sock.send((request.encode()))


c
sock.close()

