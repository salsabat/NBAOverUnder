from fastapi import FastAPI
from pydantic import BaseModel
from prediction_model import ModelRunner
import uvicorn

app = FastAPI()

class ModelInput(BaseModel):
    name: str
    stat: str
    line: str

@app.get('/')
def read_name():
    return {'prediction': 'This is not the endpoint'}

@app.post('/prediction')
def run_model_endpoint(inputs: ModelInput):
    print(inputs)
    model_runner = ModelRunner(inputs.name, inputs.stat, inputs.line)
    return {'prediction' : model_runner.run_model()}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)