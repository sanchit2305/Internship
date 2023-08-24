# Importing requirements
import socket
import pickle
import os
from collections import OrderedDict
from datetime import datetime
from queue import Queue

# Creating Response class
class respExcn:
    def __init__(self , status , timestamp):
        self.status = status
        self.timestamp = timestamp
        self.len = 2
# Creating trade message class
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

# Function to save order books to a file
def save_order_books(order_books, filename):
    # print("In save_order_books")
    with open(filename, "wb") as file:
        pickle.dump(order_books, file)

# Function to load order books from  afile
def load_order_books(filename):
        # print("In load_order_books")
        with open(filename, "rb") as file:
            return pickle.load(file)

# Function to execute a trade based on buy/sell signal
def execute_trade(order_map , order_queues , responses , asset_id , quantity , price , file_path, buy_signal , order_books , oid):

        # Check if asset exists in order_books and bid/ask sides
        if asset_id in order_books and "bid" in order_books[asset_id] or "ask" in order_books[asset_id]:
            if buy_signal:
                ask_side = order_books[asset_id]["ask"]
                bid_side = order_books[asset_id]["bid"]
                original_quantity = quantity
                remaining_quantity = quantity
                
                # Iterate through ask side ot execute trades
                for ask_price, ask_quantity in list(ask_side.items()):
                    org_ask_price = ask_price
                    org_ask_quantity = ask_quantity

                    if remaining_quantity == 0:
                        break

                    if ask_price <= price: 

                        traded_quantity = min(ask_quantity, remaining_quantity)
                        remaining_quantity -= traded_quantity
                        ask_quantity -= traded_quantity
                        if ask_quantity == 0: 
                            counter_party_oid = order_queues["ask"][ask_price].queue[0]
                            if traded_quantity >= order_map[counter_party_oid]["quantity"]:
                                fill_quantity = order_map[counter_party_oid]["quantity"]
                                order_map[counter_party_oid]["quantity"] = 0
                            else:
                                fill_quantity = traded_quantity
                                order_map[counter_party_oid]["quantity"] -= traded_quantity
                            trade_message_response = tradeMessage(datetime.now() , org_ask_price , fill_quantity , price , remaining_quantity , oid , counter_party_oid)
                            responses.append(trade_message_response)  
                            order_queues["ask"][ask_price].get() 
                            del ask_side[ask_price]
                            del order_map[counter_party_oid]
                        else:
                            ask_side[ask_price] = ask_quantity

                        if order_queues["ask"][ask_price].qsize() > 0:
                            counter_party_oid = order_queues["ask"][ask_price].queue[0]
                            if traded_quantity >= order_map[counter_party_oid]["quantity"]:
                                fill_quantity = order_map[counter_party_oid]["quantity"]
                                order_map[counter_party_oid]["quantity"] = 0
                            else:
                                fill_quantity = traded_quantity
                                order_map[counter_party_oid]["quantity"] -= traded_quantity
                            trade_message_response = tradeMessage(datetime.now() , org_ask_price , fill_quantity , price , remaining_quantity , oid , counter_party_oid)
                            responses.append(trade_message_response)  

                    
                    

                # If remaining quantity , update bid side
                if remaining_quantity > 0:
                    if price not in bid_side:
                        bid_side[price] = 0
                    bid_side[price] += remaining_quantity
                    if price in order_queues["bid"]:
                            order_queues["bid"][price].put(oid)
                    else:
                        order_queues["bid"][price] = Queue()
                        order_queues["bid"][price].put(oid)
                

                # Sort bid side
                order_books[asset_id]["bid"] = dict(sorted(bid_side.items(), key=lambda item: item[0] ,reverse=True))
            
            else:
                bid_side = order_books[asset_id]["bid"]
                ask_side = order_books[asset_id]["ask"]
                remaining_quantity = quantity
                original_quantity = quantity

                # Iterate through the bid side to execute trades
                for bid_price, bid_quantity in list(bid_side.items()):
                    org_bid_price = bid_price
                    org_bid_quantity = bid_quantity
                    if remaining_quantity == 0:
                        break

                    if bid_price >= price:

                        traded_quantity = min(bid_quantity, remaining_quantity)
                        remaining_quantity -= traded_quantity
                        bid_quantity -= traded_quantity

                        if bid_quantity == 0:
                            
                            counter_party_oid = order_queues["bid"][bid_price].queue[0]
                            if traded_quantity >= order_map[counter_party_oid]["quantity"]:
                                fill_quantity = order_map[counter_party_oid]["quantity"]
                                order_map[counter_party_oid]["quantity"] = 0
                            else:
                                fill_quantity = traded_quantity
                                order_map[counter_party_oid]["quantity"] -= traded_quantity
                            trade_message_response = tradeMessage(datetime.now() , org_bid_price , fill_quantity , price , original_quantity , oid , counter_party_oid)
                            responses.append(trade_message_response)
                            order_queues["bid"][bid_price].get()
                            del bid_side[bid_price]
                            del order_map[counter_party_oid]
                        else:
                            bid_side[bid_price] = bid_quantity
                            # if bid_price in order_queues:
                            #     order_queues[bid_price].put(oid)
                            # else:
                            #     order_queues[bid_price] = Queue()
                            #     order_queues[bid_price].put(oid)

                        if order_queues["bid"][bid_price].qsize() > 0:
                            counter_party_oid = order_queues["bid"][bid_price].queue[0]
                            if traded_quantity >= order_map[counter_party_oid]["quantity"]:
                                fill_quantity = order_map[counter_party_oid]["quantity"]
                                order_map[counter_party_oid]["quantity"] = 0
                            else:
                                fill_quantity = traded_quantity
                                print("ormp:", order_map[oid]["quantity"])
                                order_map[counter_party_oid]["quantity"] -= traded_quantity
                            
                            trade_message_response = tradeMessage(datetime.now() , org_bid_price , fill_quantity , price , traded_quantity , oid , counter_party_oid)
                            responses.append(trade_message_response)



                # If remaining quantity , update ask side
                if remaining_quantity > 0:
                    print("here in sell")
                    if price not in ask_side:
                        ask_side[price] = 0
                    ask_side[price] += remaining_quantity
                    if price in order_queues:
                            order_queues["ask"][price].put(oid)
                    else:
                        order_queues["ask"][price] = Queue()
                        order_queues["ask"][price].put(oid)
                
                

                # Sort ask side and update order_books
                order_books[asset_id]["ask"] = dict(sorted(ask_side.items(), key=lambda item: item[0]))

            # Save and update order_books
            save_order_books(order_books, file_path)

            return remaining_quantity

# Function to modify an existing order
def modify_order(order_map , oid , new_quantity , order_books , buy_signal):

    asset_id = order_map[oid]["asset_id"]
    price = order_map[oid]["price"]
    updated_quantity = abs( new_quantity - order_map[oid]["quantity"])

    # Determine the side (bid/ask) being modified
    side = "bid" if buy_signal == 1 else "ask"

    old_quantity = order_books[asset_id][side][order_map[oid]["price"]]

    # Finding the overall updated quantity for the order_book
    overall_updated_quantity = abs(updated_quantity - old_quantity)

    # If quantity becomes zero, remove the price entry from the side
    if(updated_quantity == 0):
        del order_map[oid]
        if(buy_signal == 1):
            del order_books[asset_id]["bid"][price]
        else:
            del order_books[asset_id]["ask"][price]
    # Else update the order_book with overall_updated_quantity
    else:
        if(buy_signal == 1):
            order_books[asset_id]["bid"][price] = overall_updated_quantity
        else:
            order_books[asset_id]["ask"][price] = overall_updated_quantity
    
    return updated_quantity


# Function to handle client request
def handle_client_request(client_socket , request_data , file_path , order_map , order_books, order_queues):
    responses = []

    # print("In handle_client_request")
    oid = request_data["oid"]
    asset_id = request_data["asset_id"]
    quantity = request_data["quantity"]
    price = request_data["price"]
    buy_signal = request_data["buy_signal"]
    request_no = request_data["request_no"]
    
    # Printing the order_map and order_book before request
    print("order_map Before:", order_map , '\n')
    print("OrderBookBefore:" , order_books , '\n')

    response = ""
    # Checking if the oid is present in the map or not
    if request_no == 1:
        if oid in order_map or asset_id not in order_books:
            res = respExcn(1501 , datetime.now())
            responses.append(res)
        else:
            res = respExcn(1500 , datetime.now())
            responses.append(res)
            # If oid not present in the map we update the map
            order_map[oid] = {"asset_id": asset_id, "price": price, "quantity": quantity}
            remaining_quantity = execute_trade(order_map , order_queues , responses , asset_id, quantity, price , file_path,buy_signal , order_books , oid)
            
            # Updating the remaining quantity in the map
            if remaining_quantity == 0:
                del order_map[oid]
            else:
                order_map[oid]["quantity"] = remaining_quantity
        
    elif request_no == 2:
            
            if oid not in order_map or asset_id not in order_books or order_map[oid]["quantity"] == 0:
                res = respExcn(1503 , datetime.now())
                responses.append(res)

            else:
                # Getting the new_quantity and the new_price from the request data
                res = respExcn(1502 , datetime.now())
                responses.append(res)
                new_quantity = request_data.get("quantity")
                new_price = request_data.get("price")

                if new_price is not None and new_price != order_map[oid]["price"]:
                    
                    # Deleting the previous price and quantity from the bid/ask side depending on the buy_signal
                    if buy_signal:
                        if order_books.get(order_books[asset_id]["bid"][order_map[oid]["price"]]) is not None:
                            del order_books[asset_id]["bid"][order_map[oid]["price"]]
                        else:
                            res = respExcn(1503 , datetime.now())
                            responses.append(res)

                    else:
                        if order_books.get(order_books[asset_id]["ask"][order_map[oid]["price"]]) is not None:
                            del order_books[asset_id]["bid"][order_map[oid]["ask"]]
                        else:
                            res = respExcn(1503 , datetime.now())
                            responses.append(res)

                    # Deciding the side based on buy_signal
                    side = "bid" if buy_signal == 1 else "ask"

                    # Updating the order_books by subtracting the quantity of the old price 
                    order_books[asset_id][side][order_map[oid]["price"]] -= order_map[oid]["quantity"]
                    if order_books[asset_id][side][order_map[oid]["price"]] == 0:
                        del order_books[asset_id][side][order_map[oid]["price"]]

                    # Executing a normal trade
                    remaining_quantity = execute_trade(asset_id , quantity , price , file_path, buy_signal , order_books)


                # Modifying the quantity
                elif new_quantity is not None:
                    remaining_quantity = modify_order(order_map, oid, new_quantity, order_books , buy_signal)


                order_map[oid] = {"asset_id": asset_id, "price": price, "quantity": quantity}
            
                # Sorting the order_books
                order_books[asset_id]["bid"] = dict(sorted(order_books[asset_id]["bid"].items(), key=lambda item: item[0] ,reverse=True))
                order_books[asset_id]["ask"] = dict(sorted(order_books[asset_id]["ask"].items(), key=lambda item: item[0]))

                # Saving the order_books
                save_order_books(order_books , file_path)
    
    # Handling the cancellation request
    elif request_no == 3:

        # Checking id the oid is present in order_map or not
        if oid not in order_map:

            res = respExcn(1505 , datetime.now())
            responses.append(res)

        # If the order id is present then delete from order_boooks and order_map  
        else:
            side = "bid" if buy_signal == 1 else "ask"
            del order_books[asset_id][side][order_map[oid]["price"]]
            del order_map[oid]

            res = respExcn(1504 , datetime.now())
            responses.append(res)

    # Printing the order_map and order_book after the request
    print("OrderBookAfter:" , order_books , '\n')
    print("Order_map After:" ,order_map , '\n')

    responses = pickle.dumps(responses)
    client_socket.sendall(responses)

# Configure server settings
# HOST = '192.168.15.237'  # Listen on all available interfaces
HOST = '0.0.0.0'
PORT = 12345     # Choose a suitable port number

# Create a socket server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Creating the socket
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    # Determining the file path for the order_books
    exchange_folder = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(exchange_folder, 'order_books.pkl')

    # Listening for the connections
    print("Exchange is listening for connections...")

    # Declaring order_map
    order_map = {}
    # order_map = {1: {'asset_id': 'asset1', 'price': 100, 'quantity': 50}, 2: {'asset_id': 'asset1', 'price': 99, 'quantity': 50}}
    bid_side = {}
    ask_side = {}
    order_queues = {
        "bid":bid_side,
        "ask":ask_side
    }

    # Enabling the server to listen even when one trader has closed the request
    while True: 
        conn, addr = server_socket.accept()

        with conn:

            # Connection Established
            print(f"Connected by: {addr}")
            # while True:
            data = conn.recv(1024)
            if not data:
                break

            request_data = pickle.loads(data)
            order_books = load_order_books(file_path)
            # order_books = {'asset1': {'bid': {}, 'ask': {99: 50, 100: 50}}}
            print("Request Data:", request_data , '\n')
            handle_client_request(conn , request_data , file_path , order_map , order_books , order_queues)