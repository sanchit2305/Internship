import socket
import struct
from multiprocessing import Process
import time
import zlib
# import netifaces as ni
import fcntl
import ctypes

def get_interface_ip(interface):
    try:
        # Get the IPv4 address associated with the specified interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', interface[:15].encode())
        )[20:24])
        return ip_address
    except Exception as e:
            print("Error:", e)
            return None

def receive_and_append_data(filename,max_iterations=1):
    multicast_group = '233.1.2.5'  
    multicast_port = 34330

    interface_ip = '10.10.10.3'
    # interface_name = 'enp0s3'
    # interface_ip = get_interface_ip(interface_name)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((interface_ip, multicast_port))


    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton(interface_ip))

    print(f"Listening for NSE snapshot data on {multicast_group}:{multicast_port}")

    i = True
    while i:
        try:
                with open('sample.txt' , 'a') as file:
                    # iteration = 0
                    # while iteration < max_iterations:
                        print("Before")
                        data, address = sock.recvfrom(4096)
                        print("After")
                        print(f"Received data from {address}: {len(data)}")
                        # print(data_compressed)
                        file.write(str(data) + "\n")
                        # print("data written in file")
                        decode_data(data, i)
                        # i = i + 1
                        time.sleep(1)

        except socket.error as e:
                print(f"Error receiving data: {e}")
                i = False
    


def decode_data(data , i):
    # lzo_decompress_dll = ctypes.CDLL('C:/Users/ADMIN/Desktop/Ekansh/socket_programming/decompressor.dll')
    # lzo_decompress_dll.DecompressBufferData.argtypes = [ctypes.c_void_p , ctypes.c_char_p]
    # lzo_decompress_dll.DecompressBufferData.restype = ctypes.c_int
    with open('output.txt' , 'a') as file:

        first = data[:4]

        # compression_len = data[4:6]                           
        # compression_len = struct.unpack('h' , compression_len)
        # print(compression_len)                                
        # print(data[4:])     
        # broadcast_data = data[4:]

        # print(broadcast_data)                                                  


        # decompressed_data = (ctypes.c_char * len(broadcast_data))()
        # output_size = ctypes.c_size_t(len(decompressed_data))
        # error_code = ctypes.c_int(0)

        # lzo_decompress_dll.DecompressBufferData(
        # broadcast_data, len(broadcast_data),
        # decompressed_data, output_size,
        # ctypes.byref(error_code)
        # )

        # print("data decoded")
        # print("Decompressed data: " , decompressed_data.raw.decode())

        a,b = struct.unpack('=2sh' , first)
        a = a[0]
        stri = "Set no.: " + str(i) + " cNetId:" + str(a)+ " iNoPackets:" + str(b) + "\n"

        file.write(stri)

if _name_ == "_main_":
    filename = "sample.txt"
    max_iterations = 1
    i = 1

    receive_and_append_data(filename , max_iterations)