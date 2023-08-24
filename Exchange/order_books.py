# Importing requirements
import pickle
import os
from collections import OrderedDict

# Function to create order_books.pkl
def create_order_books(order_books, filename):
    with open(filename, "wb") as file:
        pickle.dump(order_books, file)

# Creating file_path for order_books.pkl
exchange_folder = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
file_path = os.path.join(exchange_folder, 'order_books.pkl')

# Creating bid side
bid_side = {
    # 100:50,
    # 99:50,
    # 98:50
}

# Creating ask side
ask_side = {
    # 101:50,
    # 102:50,
    # 103:50
}

# Creating order_books with bid and ask side
order_books = {
    "asset1": {
        "bid":bid_side,
        "ask":ask_side
    }
}

# Calling the function to create order_books
create_order_books(order_books , file_path)