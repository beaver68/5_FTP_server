import socket
import csv
import os
from hashlib import sha256
import shutil
from threading import Thread

class User(Thread):
    def __init__(self, connection, address):
        super(User, self).__init__()
        self.conn = connection
        self.addr = address
        self.login = self.new_or_enter()

        self.conn.send('authorization is done!'.encode())

    def run(self):
        while True:
            request = conn.recv(1024).decode()
            print(request)

            if request.upper() == 'EXIT':
                break

            response = self.process(request)
            self.conn.send(response.encode())
        self.conn.close()

    def new_or_enter(self):
        self.conn.send("Do you have the account?".encode())
        request = ''.join(conn.recv(1024).decode().split())
        if request.lower() in ["yes", 'y', 'н', 'нуы', 'lf']:
            return self.enter()
        else:
            return self.create_acc()

    def enter(self):
        """
        enter to account
        :return: login
        """
        self.conn.send("       Welcome to authorization\n\nEnter the login: ".encode())
        login = conn.recv(1024).decode()
        self.conn.send("Enter the password: ".encode())
        password = sha256(conn.recv(1024)).hexdigest()

        file = 'passwords.csv'

        with open(file, 'r') as f:
            read = csv.DictReader(f, delimiter=' ')
            for line in read:
                print(line)
                if line['login'].upper() == login.upper() and line['password'].upper() == password.upper():
                    os.chdir(str(login))
                    f.close()
                    return login

        self.conn.send('Wrong login or password \nDo you want to restart enter (y/n)? '.encode())
        event = ''.join(conn.recv(1024).decode().split())

        if event.upper() in ['Y', 'YES', 'AGREE', 'DA', '']:
            return self.new_or_enter()

    def create_acc(self):
        """
         create_account
        :return: self.enter
        """
        try:
            self.conn.send("Enter the new login: ".encode())
            login = conn.recv(1024).decode()
            self.conn.send("Enter the new password: ".encode())
            password = sha256(conn.recv(1024)).hexdigest()
            login = ''.join(login.split())
            file = 'passwords.csv'
            with open(file, 'a') as f:
                f.write(login + ' ' + password + '\n')

            os.mkdir(str(login))
            return self.enter()
        except FileExistsError:
            self.conn.send("the user has already created, try to log in\nDo you want to restart enter?".encode())
            event = ''.join(conn.recv(1024).decode().split())

            if event.upper() in ['Y', 'YES', 'AGREE', 'DA', '']:
                return self.new_or_enter()



    def process(self, req):
        """
        pwd - показывает название рабочей папки
        ls - показывает содержимое рабочей папки
        cat <filename> - показывает содержимое рабочей папки
        mkdir <filename> - создает директорию
        cd <filename> - переходит в указанную директорию
        cd .. - возвращает на 1 уровень выше
        whoami - возвращает логин текущего пользователя
        rename <old> <new> - переименовывает файл
        rm <filename> - удаляет файл находящийся в папке
        rmdir <name> - удаляет указанную директорию и все файлы в ней

        """

        if req.upper() == 'PWD':
            return os.getcwd()[os.getcwd().index(self.login):]

        elif req.upper() == 'LS':
            if len(os.listdir()) == 0:
                return "files is not founded"
            return "; ".join(os.listdir())

        elif 'CAT' == req.upper().split(' ')[0]:
            if len(req.split(' ')) != 2:
                return 'name {} is not founded\nTry again!'.format(req[3:])
            else:
                return self.read_file(req.split(' ')[1])

        elif "MKDIR" == req.upper().split(' ')[0]:
            lst = req.split(" ")
            if len(lst) != 2:
                return "Error, try again, enter the correct command"
            os.mkdir(lst[1])
            return "Directory {} has created success ".format(lst[1])

        elif "CD" in req.upper():
            try:
                lst = req.split(" ")
                if len(lst) != 2:
                    return "Error, try again, enter the correct command"

                elif lst[1] == '..':
                    if len(os.getcwd()[os.getcwd().index(self.login):]) == len(self.login):
                        return "Error, use another commands"
                    for word in range(len(os.getcwd()[::-1])):
                        if os.getcwd()[word] == '\\':
                            new_dir = os.getcwd()[:word]
                            print(new_dir)
                    os.chdir(new_dir)

                    return " The current directory is {} ".format(os.getcwd()[os.getcwd().index(self.login):])

                os.chdir(lst[1])
                return " The current directory is {} ".format(lst[1])

            except FileNotFoundError:
                return "Wrong command, try again"

        elif req.upper() == "WHOAMI":
            return self.login

        elif 'RENAME' == req.upper().split(' ')[0]:
            try:
                if len(os.listdir()) == 0:
                    return "files is not founded"

                elif len(req.split(' ')) != 3:
                    return "Wrong commans, try again"

                elif req.split(' ')[1] in os.listdir():
                    os.rename(req.split(' ')[1], req.split(' ')[2])
                    return "Rename {} -> {} was success".format(req.split(' ')[1], req.split(' ')[2])

            except:
                return 'File is not founded'

        elif 'RM' == req.upper().split(' ')[0]:
            path = os.getcwd() + '\\'+ req.split(' ')[1]
            os.remove(path)
            return "File {} was deleted".format(req.split(' ')[1])

        elif 'RMDIR' == req.upper().split(' ')[0] and len(req.upper().split(' ')) == 2:
            path = os.getcwd() + '\\'+ req.split(' ')[1]
            shutil.rmtree(req.split(' ')[1])
            return "Directory {} was deleted".format(req.split(' ')[1])

        return "Command is not founded\nTry again!"


    def read_file(self, file):
        txt = ''
        with open(file, 'r') as f:
            for line in f:
                txt += line
            return txt



sock = socket.socket()
port = 9090
sock.bind(('localhost', 9090))
sock.listen(1)
print("Add port № ", port)
while True:
    conn, addr = sock.accept()
    print(addr)

    user = User(conn, addr)
    user.start()








