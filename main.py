from functools import reduce
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Tarefas(BaseModel):
    id: int | None
    responsavel: str
    descricao: str
    nivel: int          # 1,2,3,4,5
    situacao: str       # em amndamento, resolvida, pendente, cancelado
    prioridade: int     # 1,2,3


tarefas: list[Tarefas] = []


@app.post('/adicionar/')
def adicionar(item: Tarefas):
    item.id = len(tarefas) + 100
    tarefas.append(item)
    return tarefas


@app.delete('/deletar/{tarefa_id}')
def remover(tarefa_id: int):
    i = 0
    for task in tarefas:
        if task.id == tarefa_id:
            tarefas.pop(i)
            return tarefas
        i += 1


@app.get('/tarefas')
def listar():
    return tarefas


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
