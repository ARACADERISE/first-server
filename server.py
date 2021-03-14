import os, sys # os for file checking, sys for exiting
import socket, sqlite3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 18080

id_ = 0 # increments each time
database = False # started by client, if requested

server.bind((HOST,PORT))
server.listen(5) # we want to handle just 5 connections at once
print(f'Listening at ({HOST}, {PORT})\n')

while True:
    try:
        cli, addr = server.accept()
        print(f'Connection started with {addr}\n')

        cli.send(b'Hi! Here are the key commands:\nsdb -> Start Database\nclose -> close connection\n\nChoice > ')

        while cli:
            recv = cli.recv(1024)

            if recv:
                recv = recv.decode('utf-8')
                if recv == 'sdb':
                    if database == False:
                        cli.send(b'yes')
                        recv = cli.recv(1024)
                        recv = recv.decode('utf-8')

                        if recv == 'start db':
                            print(f'{addr} requested to start database\n')
                            cli.send(b'Starting Database..\n')

                            if not os.path.isfile('database.db'):
                                db = open('database.db','w')
                                db.close()

                            try:
                                id_ += 1
                                db = sqlite3.connect('database.db')
                                db_ = db.cursor()
                                db.execute('''
CREATE TABLE IF NOT EXISTS ClientInfo (
    Id INT PRIMARY KEY,
    HOST TEXT NOT NULL,
    PORT TEXT NOT NULL
);''')
                                db.execute(f'INSERT INTO ClientInfo(Id, HOST, PORT) VALUES ({id_}, "{addr[0]}", "{addr[1]}")')
                                db.commit()
                                db_.execute('SELECT * FROM ClientInfo')
                                info = db_.fetchall()
                                cli.send(b'Database successfully started!\n')
                                print(f'Successfully started the database for {addr}\nInserted info {info[0]}\n')
                                database = True
                            except:
                                cli.send(b'Failed to start the database. Something went wrong in the server\n')
                    else:
                        cli.send(b'Database already exists\n')
                if recv == 'close':
                    cli.send(b'Closing...\n')
                    print(f'Connection with {addr} has been closed.\n')
                    cli.close()
                    break
    except:
        print('Exiting...\n')
        sys.exit(0)
