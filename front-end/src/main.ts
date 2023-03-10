import axios from 'axios';

async function getTasks() {
  const response = await axios.get('http://localhost:8000/tarefas');
  return response.data;
}


const tasks = await getTasks();

const taskListElement = document.querySelector('#task-list');

//  Buscando dados
tasks.forEach(task => {
  const taskElement = document.createElement('li');
  taskElement.textContent = task.descricao;
  taskListElement.appendChild(taskElement);
});


// Enviando dados

const form = document.getElementById('create-task-form');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const taskDescription = document.getElementById('task-description').value;
  const responsavel = document.getElementById('task-responsavel').value;
  const taskPriority = document.getElementById('task-priority').value;
  const taskSituacao = document.getElementById('task-situacao').value;
  const taskNivel = document.getElementById('task-nivel').value;
  const taskData = {
    id: 0,
    responsavel: responsavel,
    descricao: taskDescription,
    nivel: taskNivel,
    situacao: taskSituacao,
    prioridade: taskPriority,
  };

  axios.post('http://localhost:8000/adicionar/', taskData)
    .then((response) => {
      console.log('Tarefa criada com sucesso:', response.data);
      // Aqui você pode redirecionar para a página de lista de tarefas ou atualizar a lista na mesma página
    })
    .catch((error) => {
      console.error('Erro ao criar tarefa:', error);
    });
});
