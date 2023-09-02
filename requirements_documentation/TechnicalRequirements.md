# Technical Requirements

## User Registration and Authentication

### User Registration Endpoint:
- HTTP Method: POST
- Path: /register
- Description: This endpoint allows users to register and create a new account.
- Request Body: User registration information (e.g., username, email, password).
- Response: A success message or relevant status code.

### User Login Endpoint:
- HTTP Method: POST
- Path: /login
- Description: This endpoint handles user login to the application.
- Request Body: User login credentials (e.g., email/username and password).
- Response: An authentication token or a relevant status code.

## Stock Market Data

### Stock Data Endpoint:

- HTTP Method: GET
- Path: /stock
- Description: This endpoint provides real-time stock market data for stocks listed sin the DASDAQ and DUNEMI markets.
- Response: Stock market data.

### Historical Stock Data Endpoint:

- HTTP Method: GET
- Path: /stock/{id}
- Description: This endpoint provides access to historical data to a specific stock for analysis purposes.
- Response: Historical data to a specific stock for analysis purposes.

## Buying Stocks

### Buy Order Placement Endpoint:

- HTTP Method: POST
- Path: /buy
- Description: This endpoint allows users to place buy orders for stocks with specified details.
- Request Body: Buy order information (e.g., stock symbol, quantity, price).
- Response: A success message or relevant status code indicating the outcome of the buy order placement.

#### Validation
- The API must validate if the Request Body is acceptable.
- The API must validate if the Stock passed on the Request Body exists.
- The API must validate that users have sufficient funds in their account to make the purchase.


## User Portfolio

### User Portfolio Retrieval Endpoint:

- HTTP Method: GET
- Path: /portfolio
- Description: This endpoint retrieves portfolio information for a specific user.
- Response: Portfolio data for the specified user, including stock symbol, quantity owned, and average purchase price for each stock.


## Selling Stocks

### Sell Order Placement Endpoint:

- HTTP Method: POST
- Path: /sell
- Description: This endpoint allows users to place sell orders for stocks they own.
- Request Body: Sell order information (e.g., stock symbol, quantity).
- Response: A success message or relevant status code indicating the outcome of the sell order placement.

#### Validation

- The API must validate if the Request Body is acceptable.
- The API must validate if the Stock passed on the Request Body exists.
- The API must validate that users own the stocks they are attempting to sell.
