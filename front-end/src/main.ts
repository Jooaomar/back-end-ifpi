// const jsonResponse = await fetch("http://localhost:8000/tarefas");
// const jsonData = await jsonResponse.json();
// console.log(jsonData);


const textResponse = await fetch("http://localhost:8000/tarefas");
const textData = await textResponse.text();
document.getElementById("tarefas-div").innerHTML = textData;


