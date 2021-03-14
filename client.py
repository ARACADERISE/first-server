import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 18080))
data = client.recv(1024)
data = data.decode('utf-8')
print(data)

while True:
    try:
        choice = input('Input Something: ')
        if choice == '':
            while choice == '':
                choice = input('Input Something: ')

        client.send(choice.encode('utf-8'))
        resp = client.recv(1024)
        if choice == 'sdb':
            if resp.decode('utf-8') == 'yes':
                print('here~!')
                client.send(b'start db')
                resp = client.recv(1024)
                print(resp.decode('utf-8'))

                # success, or failure, msg
                sofm = client.recv(1024)
                print(sofm.decode('utf-8'))
            else:
                print(resp.decode('utf-8'))
        if choice == 'close':break
        else: continue
    except:
        break
client.close()
