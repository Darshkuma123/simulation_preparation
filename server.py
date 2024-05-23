import socket

Host='127.0.0.1'
port=65432


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((Host,port))
    s.listen()
    conn,addr=s.accept()
    with conn:
        #data= conn.recv(1024)
        print("connected by {addr}")
        while True:
            conn.sendall(b'1')
            #print(data)
            #if not data:
                #break
            #conn.sendall(data)