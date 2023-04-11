from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Union
import pymongo
from fastapi.responses import JSONResponse
from bson import json_util
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('USER')
password = os.getenv('PASSWORD')


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "http://0.0.0.0:3000/",
    "http://localhost:3000/",
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@cluster0.ms2ogne.mongodb.net/?retryWrites=true&w=majority")
db = client["listaFilmes"]
collection = db["filme"]


class Tarefas(BaseModel):
    id: Union[int, None]
    responsavel: str
    descricao: str
    nivel: int          # 1,2,3,4,5
    situacao: str       # em amndamento, resolvida, pendente, cancelado
    prioridade: int     # 1,2,3


tarefas: list[Tarefas] = []


@app.post('/adicionar/')
def adicionar(item: Tarefas):
    item.id = len(tarefas) + 100
    # tarefas.append(item)
    col = dict(item)
    collection.insert_one(col)
    return item


@app.delete('/deletar/{tarefa_id}')
def remover(tarefa_id: int):
    i = 0
    for task in tarefas:
        if task.id == tarefa_id:
            tarefas.pop(i)
            return tarefas
        i += 1


@app.get('/filmes')
def listar():
    filmes = []
    for filme in collection.find():
        filmes.append(json_util.dumps(filme))
    return filmes


@app.get('/tarefas/')
def listar_situacao(situacao: str):
    selects = []
    for task in tarefas:
        if task.situacao == situacao:
            selects.append(task)
    if len(selects) > 0:
        return selects
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get('/tarefas-nivel/')
def listar_nivel(nivel: int):
    selects = []
    for task in tarefas:
        if task.nivel == nivel:
            selects.append(task)
    if len(selects) > 0:
        return selects
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get('/tarefas-prioridade/')
def listar_prioridade(prioridade: int):
    selects = []
    for task in tarefas:
        if task.prioridade == prioridade:
            selects.append(task)
    if len(selects) > 0:
        return selects
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get('/detalhes/{tarefa_id}')
def detalhes(tarefa_id: int):

    for task in tarefas:
        if task.id == tarefa_id:
            return task


@app.put('/situacao/{tarefa_id}')
def situacao(tarefa_id: int, mudanca: str):

    for task in tarefas:
        if task.id == tarefa_id:
            task.situacao = mudanca
            return task

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)