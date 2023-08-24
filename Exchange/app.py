from flask import Flask, render_template, request
import socket
import pickle
import os 

app = Flask(__name__)

# Configure trader settings
SERVER_IP = socket.gethostname()  # Replace with the exchange's IP address
SERVER_PORT = 12345   # Replace with the exchange's port

current_directory = os.getcwd()

print("Current Working Directory:", current_directory)

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

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_trade', methods=['POST'])
def submit_trade():
    # Get form data from request
    oid = int(request.form['oid'])
    asset_id = request.form['asset_id']
    quantity = int(request.form['quantity'])
    price = int(request.form['price'])
    buy_signal = int(request.form['buy_signal'])
    request_no = int(request.form['request_no'])

    # Simulate trader sending a trade request
    trade_data = {
        "oid": oid,
        "asset_id": asset_id,
        "quantity": quantity,
        "price": price,
        "buy_signal": buy_signal,
        "request_no": request_no
    }

    # Send trade request to server
    response = send_trade_request(trade_data)

    return render_template('index.html', response=response)

# Function to send trade request to server
def send_trade_request(trade_data):
    # Similar to your existing code to send trade request to the server
    # ...
    # Return the response or appropriate message
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

        return response

if __name__ == '__main__':
    app.run(debug=False)











