# Exchange System Documentation

This documentation provides an overview of the components, functionality, and usage instructions for the exchange system implemented in the provided Python code.

## 1. Introduction

The provided Python code implements a simplified exchange system consisting of an exchange server, a trader interface, and order book initialization. Traders can use the trader interface to submit trade requests to the exchange server. The exchange server handles trade execution, maintains order books, and provides responses to traders.

## 2. Components

### Exchange Server

The exchange server (`exchange_code.py`) is responsible for receiving and processing trade requests from traders. It executes trades based on buy and sell signals, updates order books, and sends response messages to traders.

### Trader Interface

The trader interface (`app.py`) is a web application that allows traders to submit trade requests to the exchange server. Traders can enter order details such as order ID, asset ID, quantity, price, buy/sell signal, and request type. The interface communicates with the exchange server to send trade requests and display response messages.

### Order Book Initialization

The `order_book.py` script initializes the order books for the exchange system. It creates order book data structures for bid and ask sides of assets.

## 3. Usage

### Initializing the order_books
1. Open a terminal window.

2. Navigate to the directory containing `order_books.py`

3. Run the following command to initialize the order_books:
```bash
   python order_books.py
```

### Running the Exchange Server

1. Open a terminal window.

2. Navigate to the directory containing `exchange.py`.

3. Run the following command to start the exchange server:
```bash
   python exchange.py
```
4. The exchange server will start listening for connections.

### Using the Trader Interface
1. Open a terminal window

2. Navigate to the directory containing `app.py`

3. Run the following command to start the server:
```bash
    python app.py
```
4. Open a web browser.

5. Access the trader interface by entering the following URL:
```bash
http://127.0.0.1:5000/
```

6. Fill in the trade request form with order details.

7. Click the "Submit Trade" button to send the trade request to the exchange server.

8. The trader interface will display response messages from the server, including trade execution details and status.

## 4. Code Explanation

### Exchange Server Code Explanation

The exchange server code (`exchange_code.py`) handles incoming trade requests, executes trades, and updates order books. It contains classes for `respExcn` (response exception), `tradeMessage` (trade execution details), and functions for trade execution, order book management, and client request handling.

### Trader Interface Code Explanation

The trader interface code (`app.py`) is a Flask web application that provides a user interface for traders to submit trade requests. It communicates with the exchange server using sockets to send and receive trade data and response messages.

### Order Book Initialization Code Explanation

The order book initialization script (`order_book.py`) creates initial order book data structures for assets, including bid and ask sides.

## 5. Dependencies

The provided code uses the following Python libraries:

- `socket`: For socket communication between the exchange server and trader interface.
- `pickle`: For serializing and deserializing Python objects.
- `Flask`: For creating the trader interface web application.
- `os`: For file operations and path manipulation.

## 6. Contributors

- [Sanchit Dhawan](https://github.com/sanchit2305)


---

