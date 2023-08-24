import socket
import struct

msg_length = 32
home_team_goals = 4
away_team_goals = 3
home_team_saves = 2
away_team_saves = 1
home_team_fouls = 0
away_team_fouls = 1

temp = 1

packed_data = struct.pack('=iqqiihh', msg_length, home_team_goals, away_team_goals, home_team_saves, away_team_saves, home_team_fouls, away_team_fouls)
print(len(packed_data))


def server_program():
    host = '192.168.15.241'
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host,port))

    server_socket.listen(3)
    conn,address = server_socket.accept()
    print("connection from: ", str(address))
    total = []
    i=0
    for i in range(13100):
        
        conn.send(packed_data)
        total.append(packed_data)
        i = i+1
    
    total_bytes = b"".join(total)
    print(len(total_bytes))
    # conn.sendall(total_bytes)
    conn.send(b"Terminate")
    print("Sent")
    conn.close()        


if __name__ == '__main__':
    server_program()