# FastAPI-demo
FastAPI demo

## Development Mode
FastAPI does not come with a server (unlike Flask), so we need to use uvicorn. Run the following command to start it
```
(env)$ uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8008
```

To make a API call, use the following command
```
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"ticker":"MSFT"}' \
  http://localhost:8008/predict
```


## Production Mode
Use Heroku

more on https://testdriven.io/blog/fastapi-machine-learning/
