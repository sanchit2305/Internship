# Importing requirements
import socket
import pickle

class respExcn:
    def __init__(self, status, timestamp):
        self.status = status
        self.timestamp = timestamp
        self.len = 2

class tradeMessage:
    def __init__(self , timestamp , fillPrice , fillQuantity , order_price , order_quantity , oid , counter_party_oid):
        self.timestamp = timestamp
        self.fillPrice = fillPrice
        self.fillQuantity = fillQuantity
        self.order_price = order_price
        self.order_quantity = order_quantity
        self.order_oid = oid
        self.counter_party_oid = counter_party_oid
        self.len = 5

# Configure trader settings
SERVER_IP = socket.gethostname()  # Replace with the exchange's IP address
SERVER_PORT = 12345   # Replace with the exchange's port

# Connecting to exchange server
def send_trade_request(trade_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        serialized_data = pickle.dumps(trade_data)
        client_socket.sendall(serialized_data)
        # while True:
        response = client_socket.recv(1024)
        response = pickle.loads(response)
        # print(response.len)
        # print("Server response:")
        # print("Status:" , response.status)
        # print("Time:", response.timestamp)
        if len(response) == 1:
            print("Server response:")
            print("Status:", response[0].status)
            print("Time:", response[0].timestamp)
        else:
            print("Server response:")
            print("Status:", response[0].status)
            print("Time:", response[0].timestamp)
            print('\n')
            for i in range(1 , len(response)):
                # print()
                print("Trade Message:")
                print("Time:", response[i].timestamp)
                print("fillPrice:", response[i].fillPrice)
                print("fillQuantity:", response[i].fillQuantity)
                print("order_price:", response[i].order_price)
                print("order_quantity:", response[i].order_quantity)
                print("oid:", response[i].order_oid)
                print("Counter_party_oid:" , response[i].counter_party_oid)
                print('\n')


# Simulate trader sending a trade request
trade_data = {
    "oid":2,                # OrderId
    "asset_id": "asset1",   # AssetId
    "quantity":50,          # Quantity of the asset
    "price":100,           # Price of the asset
    "buy_signal":0,        # 1 to buy 0 to sell
    "request_no":3     # 1 for new , 2 for modify , 3 for cancel
}

# Function to send data to server
send_trade_request(trade_data)