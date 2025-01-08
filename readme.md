## risk-intelligence-reference-app

### Install dependencies and run the app

```shell
python3 -m venv .venv
```

```shell
. .venv/bin/activate
```

```shell
pip install -r requirements.txt
```

```shell
cp .env.example .env
```

```shell
flask run
```

### Run tests

```shell
pytest
```