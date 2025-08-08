# Trading System

Welcome to the Trading System Repository! This repository focus on the development of a robust trading system, leveraging low latency strategies.

## Description

Trading System is a microservices-based application designed to enable seamless trading across multiple markets—such as crypto and stocks—and various exchanges, including B3, CME, Nasdaq, Coinbase, and Binance.

The system follows industry best practices, adopting Domain-Driven Design (DDD) and an Event-Driven Architecture (EDA). This separation ensures that client-side logic minimally affects backend processes, making the codebase more approachable for new developers.

At its core, the platform uses a central Redis broker to dispatch events, triggering algorithmic actions such as updating stock market prices or sending hedge orders in the crypto market. Each algorithm runs in its own isolated process, ensuring that a failure in one strategy does not impact the overall system’s operation.

Users can interact with the system in two primary ways:

- Direct Order Submission: Clients send orders to the OrderService for immediate execution.
- Algorithmic Trading: Clients develop custom algorithms handled by the AlgoService, which communicates with the OrderService via REST API.

This architecture ensures high resilience, scalability, and flexibility for both manual and automated trading workflows.

## Architecture

![Service's Architecture](https://github.com/estudart/estudart-trading-system/blob/main/docs/trading-diagram.jpeg)

## Api Docs

![Service's Architecture](https://github.com/estudart/estudart-trading-system/blob/main/docs/rest-api.png)

## Features

- **Multi-market support**: Trade seamlessly across crypto and stock markets.
- **Multi-exchange integration**: Connect to exchanges like B3, CME, Nasdaq, Coinbase, and Binance.
- **Algorithmic trading**: Deploy custom trading strategies with isolated processes for fault tolerance.
- **Event-driven execution**: Real-time event dispatching via Redis for lightning-fast order handling.
- **Flexible order management**: Send orders manually or through automated algorithms.

## Installation

To run the StreetFighters app locally, follow these steps:

1. Clone this repository to your local machine using:
    ```bash
    git clone https://github.com/estudart/estudart-trading-system

2. Setup the .env file for each service:
    ```bash
    ENV=DEV

    # DEV KEYS

    # ORDER SERVICE CLIENT
    ORDER_SERVICE_URL_DEV=http://localhost:5000/api/v1

    # BINANCE
    BINANCE_API_KEY_DEV=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    BINANCE_API_SECRET_DEV=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    BINANCE_ENDPOINT_DEV=https://testnet.binance.vision/api

    BINANCE_UI=https://testnet.binancefuture.com/en-IN/futures/BTCUSDT
    BINANCE_FUTURES_API_KEY_DEV=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    BINANCE_FUTURES_API_SECRET_DEV=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    BINANCE_FUTURES_ENDPOINT_DEV=https://testnet.binancefuture.com/fapi

    BINANCE_MD_ENDPOINT_DEV=https://api.binance.com/api/v3/ticker

    # COINBASE
    COINBASE_DOLLAR_ENDPOINT_DEV=https://api.coinbase.com/v2

    # FLOWA
    FLOWA_API_SECRET_DEV=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    FLOWA_CLIENT_ID_DEV=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    FLOWA_ENDPOINT_DEV=https://mtbserver-staging.americastg.com.br:51511/api
    FLOWA_TOKEN_ENDPOINT_DEV=https://mtbserver-Staging.americastg.com.br:51525/connect/token
    FLOWA_USERNAME_DEV=xxxxxxxxxxxxxxxxxxxxxxxxx
    FLOWA_PASSWORD_DEV=xxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # HASHDEX
    HASHDEX_MD_ENDPOINT_DEV=https://api2.hashdex.io/marketdata/v2

    # REDIS
    REDIS_HOST_DEV=redis-db
    REDIS_PORT_DEV=6379

3. Build and run all services:
    ```bash
    docker-compose up --build

## Usage

- **OrderService**: Send manual orders to be executed immediately.
- **AlgoService**: Deploy your own algorithms, which will communicate with OrderService via REST API.
- **Market data updates**: Listen to Redis events for real-time price updates and trade executions.
- **Fault tolerance**: Algorithms run in isolated processes to ensure system stability.

## Technologies Used

- Python
- Flask
- Redis
- Docker
- REST API
- Domain-Driven Design (DDD)
- Event-Driven Architecture (EDA)

## Contributing

Contributions are welcome!
If you encounter bugs or have suggestions for new features, please open an issue in the [GitHub repository](https://github.com/estudart/StreetFighters) or submit a pull request.