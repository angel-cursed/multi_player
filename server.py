import socket
import _thread
import sys

server = "192.168.1.138"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("-------- Waiting For Connections --------")

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print("Disconnected")
                break
            reply = data.decode("utf-8")
            print("Received: " + reply)
            if reply == "exit":
                break
            conn.sendall(str.encode(reply))
        except socket.error:
            break

    print("Lost Connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: " + addr[0] + " : " + str(addr[1]))

    _thread.start_new_thread(threaded_client, (conn,))