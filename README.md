Create virtual env and install dependencies

```
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the server
```
uvicorn "main:app" --reload --host 0.0.0.0 --port 8000
```
