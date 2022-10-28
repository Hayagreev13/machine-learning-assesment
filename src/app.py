import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from solution import extract_entities

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Welcome fellow extractor! This is an application to extract details from event titles'}

@app.post('/extract_from_realtime')
def process_json_input(data:str):
    return extract_entities(data)

@app.post('/extract_from_batch')
def process_json_input(data:list):
    json_out = []
    for event in data:
        json_out.append(extract_entities(event))
    return json_out


#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload