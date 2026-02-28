from fastapi import FastAPI

app = FastAPI()

@app.get('/test')
def get_app_name(name: str):
    return 'Hello Vijay'