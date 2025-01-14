# GrailPay Risk Intelligence API Reference Application

Company Website: (https://grailpay.com)

## Purpose

This application is a reference implementation of the GrailPay Risk Intelligence API. It demonstrates how to:

* Verify account and routing numbers.

## Installation

This project was developed using Python 3.12.6.

### Initiate and activate new virtual environment

```shell
python3 -m venv .venv
```

```shell
. .venv/bin/activate
```

### Install dependencies

```shell
pip install -r requirements.txt
```

```shell
cp .env.example .env
```

### Run the app
```shell
flask run -p 3000
```

### Run tests

```shell
pytest
```

### Call services

#### Account Routing Verify service

```shell
curl -X POST http://localhost:3000/verify \
-H "Content-Type: application/json" \
-d '{
  "account_number": "your_account_number",
  "routing_number": "your_routing_number",
  "token": "your_token"
}'
```