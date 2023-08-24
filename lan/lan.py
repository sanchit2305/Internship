import socket
import struct
from multiprocessing import Process
import time
import zlib
import lzo
def receive_and_append_data(filename,max_iterations=1):
    multicast_group = '233.1.2.5'  
    multicast_port = 34330  

    interface_ip = '10.10.10.104'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((interface_ip, multicast_port))


    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))

    print(f"Listening for NSE snapshot data on {multicast_group}:{multicast_port}")

    i = 1
    while True:
        try:
                with open('sample.txt' , 'a') as file:
                        data, address = sock.recvfrom(4096)
                        print(f"Received data from {address}: {len(data)}")
                        
                        print(len(data))
                        file.write(str(data) + "\n")
                        print("data written in file")
                        time.sleep(1)
                        decode_data(data, i)
                        i = i + 1
                        time.sleep(1)
        except socket.error as e:
                print(f"Error receiving data: {e}")
    
class Output:
    def __init__(self,cNetId , iNoPackets):
        self.cNetId = cNetId
        self.iNoPackets = iNoPackets

def decode_data(data , i):
    
    with open('output.txt' , 'a') as file:
         
        
        first = data[:4]
        remaining_data = data[4:]
        compression_len = data[4:6]
        compression_len = struct.unpack('h' , compression_len)
        print(compression_len)
        print(first)
        a,b = struct.unpack('=2sh' , first)
        a = a[0]
        stri = "Set no.: " + str(i) + " cNetId:" + str(a)+ " iNoPackets:" + str(b) + "\n"
        
        file.write(stri) 


        while len(remaining_data) > 0:
            compressed_size = struct.unpack('H', remaining_data[:2])[0]
            compressed_block = remaining_data[2:2 + compressed_size]

            print("Compressed Block:", compressed_block)

        # if len(remaining_data) > 0:
        #     print("Remaining Data Length:", len(remaining_data))

            try:
                
                decompressed_data = lzo.decompress(compressed_block)
                
                for byte in decompressed_data:
                    print(hex(byte), end=' ')
                print()
                remaining_data = remaining_data[2 + compressed_size:]  
                
            except lzo.error as e:
                print("LZO decompression error:", e)
                break
        
if __name__ == "__main__":
    filename = "sample.txt"
    max_iterations = 1
    i = 1
        
    receive_and_append_data(filename , max_iterations)
